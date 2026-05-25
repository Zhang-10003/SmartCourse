from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from models import AsyncSessionFactory, KnowledgeBase
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import re
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('rag_router')
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/api", tags=["rag"])

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)


def extract_text_from_file(file_path: str, file_ext: str) -> str:
    """根据文件类型提取纯文本"""
    try:
        if file_ext == "pdf":
            import fitz
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        elif file_ext == "docx":
            import docx
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        elif file_ext == "txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
    except Exception as e:
        logger.error(f"文本提取失败 {file_path}: {e}")
    return ""


def clean_and_chunk(text: str, chunk_size: int = 512, overlap: int = 64) -> list:
    """清洗文本并按固定大小分块（带重叠窗口）"""
    text = re.sub(r'\s+', ' ', text).strip()
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c for c in chunks if c.strip()]


async def vectorize_file(file_id: int, file_path: str, file_ext: str):
    """异步：提取文本 → 清洗分块 → embedding → 写入 Chroma"""
    try:
        logger.info(f"[RAG] 开始向量化文件 {file_id}")
        text = extract_text_from_file(file_path, file_ext)
        if not text:
            logger.warning(f"[RAG] 文件 {file_path} 未提取到文本")
            return
        chunks = clean_and_chunk(text)
        logger.info(f"[RAG] 文件 {file_path} 提取到 {len(chunks)} 个文本块")

        from core.rag.rag_service import RAGService
        rag = RAGService()
        rag.add_knowledge(chunks)
        logger.info(f"[RAG] Chroma 写入完成，共 {len(chunks)} 条")

        async with AsyncSessionFactory() as session:
            result = await session.execute(select(KnowledgeBase).filter(KnowledgeBase.id == file_id))
            kb = result.scalar_one_or_none()
            if kb:
                kb.embedding_status = 1
                await session.commit()
                logger.info(f"[RAG] 文件 {file_id} embedding_status 更新为 1")
        logger.info(f"[RAG] 向量化完成 file_id={file_id}")

    except Exception as e:
        logger.error(f"[RAG] 向量化失败 file_id={file_id}: {e}")
        import traceback
        logger.error(traceback.format_exc())


class KnowledgeBaseResponse(BaseModel):
    id: int
    file_name: str
    file_type: str
    file_size: int
    status: int
    upload_time: str


class KnowledgeBaseListResponse(BaseModel):
    code: int
    data: List[KnowledgeBaseResponse]
    message: str


async def get_db_session():
    async with AsyncSessionFactory() as session:
        yield session


@router.get("/rag/knowledge-base", response_model=KnowledgeBaseListResponse)
async def get_knowledge_base(
    file_type: Optional[str] = Query(None, description="文件类型筛选：pdf/docx/txt")
):
    """获取知识库文件列表"""
    try:
        async with AsyncSessionFactory() as session:
            query = select(KnowledgeBase)
            
            if file_type and file_type.lower() in ["pdf", "docx", "txt"]:
                query = query.filter(KnowledgeBase.file_type == file_type.lower())
            
            result = await session.execute(query)
            files = result.scalars().all()
            
            file_list = []
            for file in files:
                file_list.append({
                    "id": file.id,
                    "file_name": file.file_name,
                    "file_type": file.file_type,
                    "file_size": file.file_size,
                    "status": file.status,
                    "upload_time": file.upload_time.strftime("%Y-%m-%d %H:%M:%S")
                })
            
            return {"code": 200, "data": file_list, "message": "success"}
    
    except Exception as e:
        logger.error(f"获取知识库列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取知识库列表失败: {str(e)}")


@router.post("/rag/knowledge-base")
async def upload_file(file: UploadFile = File(...)):
    """上传知识库文件"""
    try:
        # 调试日志：打印接收到的文件信息
        logger.info(f"========== 开始处理上传请求 ==========")
        logger.info(f"文件名: {file.filename}")
        logger.info(f"文件类型(MIME): {file.content_type}")
        logger.info(f"文件大小(原始): {file.size}")
        logger.info(f"ASSETS_DIR: {ASSETS_DIR}")
        logger.info(f"ASSETS_DIR是否存在: {os.path.exists(ASSETS_DIR)}")
        
        # 确定文件类型（主要依靠扩展名判断）
        file_ext = file.filename.split(".")[-1].lower()
        logger.info(f"文件扩展名: {file_ext}")
        
        # 验证文件扩展名
        if file_ext not in ["pdf", "docx", "txt"]:
            logger.error(f"文件扩展名不允许: {file_ext}")
            raise HTTPException(status_code=400, detail=f"不支持的文件扩展名: {file_ext}，仅支持 pdf, docx, txt")
        
        # 辅助验证MIME类型（放宽限制，因为不同系统可能发送不同的MIME类型）
        allowed_types = [
            "application/pdf", 
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
            "text/plain",
            "application/octet-stream",  # 某些系统会发送这个
            "text/plain; charset=UTF-8"
        ]
        logger.info(f"文件类型(MIME): {file.content_type}")
        logger.info(f"允许的MIME类型: {allowed_types}")
        
        if file.content_type not in allowed_types:
            logger.warning(f"MIME类型不在白名单中，但扩展名符合要求: {file.content_type}")
            # 不拒绝，只记录警告
        
        # 保存文件
        file_path = os.path.join(ASSETS_DIR, file.filename)
        logger.info(f"保存路径: {file_path}")
        file_size = 0
        
        try:
            with open(file_path, "wb") as f:
                logger.info("开始读取文件内容...")
                chunk_count = 0
                while True:
                    chunk = await file.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    file_size += len(chunk)
                    chunk_count += 1
                    if chunk_count % 100 == 0:
                        logger.info(f"已读取 {chunk_count * 1024} 字节...")
                logger.info(f"文件读取完成，共 {chunk_count} 块，总大小: {file_size} 字节")
        except Exception as save_error:
            logger.error(f"保存文件失败: {str(save_error)}")
            raise HTTPException(status_code=500, detail=f"保存文件失败: {str(save_error)}")
        
        # 保存到数据库（注意：这里需要传入真实的 teacher_id）
        try:
            logger.info("开始保存到数据库...")
            async with AsyncSessionFactory() as session:
                kb_file = KnowledgeBase(
                    teacher_id=1,  # TODO: 需要从认证信息获取真实的 teacher_id
                    file_name=file.filename,
                    file_type=file_ext,
                    file_size=file_size,
                    file_path=file_path,
                    status=1,
                    embedding_status=0
                )
                session.add(kb_file)
                await session.commit()
                await session.refresh(kb_file)
                logger.info(f"数据库保存成功，记录ID: {kb_file.id}")
        except Exception as db_error:
            logger.error(f"保存数据库失败: {str(db_error)}")
            # 删除已保存的文件
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info("已删除部分上传的文件")
            raise HTTPException(status_code=500, detail=f"保存数据库失败: {str(db_error)}")
        
        logger.info(f"========== 文件上传成功 ==========")

        asyncio.create_task(vectorize_file(kb_file.id, file_path, file_ext))
        
        return JSONResponse(
            status_code=200,
            content={
                "code": 200,
                "data": {
                    "id": kb_file.id,
                    "file_name": kb_file.file_name,
                    "file_type": kb_file.file_type,
                    "file_size": kb_file.file_size,
                    "status": kb_file.status,
                    "upload_time": kb_file.upload_time.strftime("%Y-%m-%d %H:%M:%S")
                },
                "message": "文件上传成功"
            }
        )
    
    except HTTPException as e:
        logger.error(f"HTTP异常: {e.status_code} - {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        logger.error(f"异常类型: {type(e).__name__}")
        import traceback
        logger.error(f"异常堆栈:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")


@router.delete("/rag/knowledge-base/{file_id}")
async def delete_file(file_id: int):
    """删除知识库文件"""
    try:
        async with AsyncSessionFactory() as session:
            result = await session.execute(select(KnowledgeBase).filter(KnowledgeBase.id == file_id))
            kb_file = result.scalar_one_or_none()
            
            if not kb_file:
                raise HTTPException(status_code=404, detail="文件不存在")
            
            # 删除物理文件
            if os.path.exists(kb_file.file_path):
                os.remove(kb_file.file_path)
            
            # 删除数据库记录
            await session.delete(kb_file)
            await session.commit()
            
            logger.info(f"文件删除成功: {kb_file.file_name}")
            
            return {"code": 200, "data": None, "message": "文件删除成功"}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"文件删除失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文件删除失败: {str(e)}")


@router.get("/rag/knowledge-base/stats")
async def get_knowledge_base_stats():
    """获取知识库统计信息"""
    try:
        async with AsyncSessionFactory() as session:
            # 统计总文件数和总大小
            total_count = await session.execute(select(func.count(KnowledgeBase.id)))
            total_size = await session.execute(select(func.sum(KnowledgeBase.file_size)))
            
            # 按类型统计
            pdf_count = await session.execute(
                select(func.count(KnowledgeBase.id)).filter(KnowledgeBase.file_type == "pdf")
            )
            docx_count = await session.execute(
                select(func.count(KnowledgeBase.id)).filter(KnowledgeBase.file_type == "docx")
            )
            txt_count = await session.execute(
                select(func.count(KnowledgeBase.id)).filter(KnowledgeBase.file_type == "txt")
            )
            
            return {
                "code": 200,
                "data": {
                    "total_count": total_count.scalar_one_or_none() or 0,
                    "total_size": total_size.scalar_one_or_none() or 0,
                    "pdf_count": pdf_count.scalar_one_or_none() or 0,
                    "docx_count": docx_count.scalar_one_or_none() or 0,
                    "txt_count": txt_count.scalar_one_or_none() or 0
                },
                "message": "success"
            }
    
    except Exception as e:
        logger.error(f"获取统计信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")
