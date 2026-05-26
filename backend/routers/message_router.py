from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime

from models import Message, Assignment
from dependencies import get_session

router = APIRouter(prefix="/api", tags=["messages"])

@router.get("/students/{student_id}/messages", response_model=dict)
async def get_student_messages(
    student_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取学生的所有消息"""
    try:
        # 查询学生的消息，关联作业信息
        stmt = select(Message, Assignment).outerjoin(
            Assignment, Message.assignment_id == Assignment.assignment_id
        ).where(Message.student_id == student_id).order_by(Message.created_at.desc())
        
        result = await session.execute(stmt)
        rows = result.all()
        
        messages = []
        for message, assignment in rows:
            message_dict = {
                "message_id": message.message_id,
                "student_id": message.student_id,
                "assignment_id": message.assignment_id,
                "content": message.content,
                "type": message.type,
                "is_read": message.is_read,
                "created_at": message.created_at.isoformat() if hasattr(message.created_at, 'isoformat') else str(message.created_at)
            }
            
            # 根据消息类型和作业信息设置标题
            if message.type == "assignment_deadline":
                message_dict["title"] = "作业截止"
            elif message.type == "course_change":
                message_dict["title"] = "课程变动通知"
            elif message.type == "homework_reminder":
                message_dict["title"] = "作业提醒"
            elif message.type == "system_update":
                message_dict["title"] = "系统更新"
            else:
                message_dict["title"] = "通知"
            
            messages.append(message_dict)
        
        return {
            "success": True,
            "data": messages
        }
    except Exception as e:
        print(f"获取学生消息失败: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "获取消息失败"
        }

@router.put("/messages/{message_id}/read", response_model=dict)
async def mark_message_as_read(
    message_id: int,
    session: AsyncSession = Depends(get_session)
):
    """标记消息为已读"""
    try:
        # 查询消息
        stmt = select(Message).where(Message.message_id == message_id)
        result = await session.execute(stmt)
        message = result.scalar_one_or_none()
        
        if not message:
            raise HTTPException(status_code=404, detail="消息不存在")
        
        # 更新为已读
        message.is_read = True
        await session.commit()
        await session.refresh(message)
        
        return {
            "success": True,
            "data": {
                "message_id": message.message_id,
                "is_read": message.is_read
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        print(f"标记消息已读失败: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "标记失败"
        }

@router.put("/students/{student_id}/messages/read-all", response_model=dict)
async def mark_all_messages_as_read(
    student_id: int,
    session: AsyncSession = Depends(get_session)
):
    """标记学生的所有消息为已读"""
    try:
        # 更新所有未读消息
        stmt = update(Message).where(
            Message.student_id == student_id,
            Message.is_read == False
        ).values(is_read=True)
        
        result = await session.execute(stmt)
        await session.commit()
        
        return {
            "success": True,
            "data": {
                "updated_count": result.rowcount
            }
        }
    except Exception as e:
        await session.rollback()
        print(f"标记所有消息已读失败: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "标记失败"
        }
