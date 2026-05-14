import os
from typing import List, Dict, Optional
import chromadb
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings
from .embedding import DashScopeEmbedding


class DashScopeChromaEmbedding(EmbeddingFunction):
    """兼容 ChromaDB 的 DashScope Embedding"""
    
    def __init__(self, embedding: DashScopeEmbedding):
        self.embedding = embedding
    
    def __call__(self, input: Documents) -> Embeddings:
        return self.embedding.embed_batch(input)


class VectorDB:
    """向量数据库（使用 ChromaDB + DashScope Embedding）"""
    
    def __init__(self, collection_name: str = "knowledge_base"):
        """
        初始化向量数据库
        
        Args:
            collection_name: 集合名称
        """
        self.collection_name = collection_name
        self.db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
        os.makedirs(self.db_path, exist_ok=True)
        
        # 初始化 Embedding
        self.embedding = DashScopeEmbedding()
        self.ef = DashScopeChromaEmbedding(self.embedding)
        
        # 初始化 ChromaDB
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # 获取或创建集合
        try:
            self.collection = self.client.get_collection(
                name=collection_name,
                embedding_function=self.ef
            )
        except Exception:
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.ef
            )
    
    def add_documents(self, documents: List[str], metadatas: Optional[List[Dict]] = None, ids: Optional[List[str]] = None):
        """
        添加文档到数据库
        
        Args:
            documents: 文档内容列表
            metadatas: 元数据列表
            ids: ID 列表
        """
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        if metadatas is None:
            metadatas = [{} for _ in documents]
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(self, query_text: str, n_results: int = 5) -> Dict:
        """
        查询相关文档
        
        Args:
            query_text: 查询文本
            n_results: 返回结果数量
            
        Returns:
            查询结果字典
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return {
            'documents': results['documents'][0] if results['documents'] else [],
            'metadatas': results['metadatas'][0] if results['metadatas'] else [],
            'distances': results['distances'][0] if results['distances'] else [],
            'ids': results['ids'][0] if results['ids'] else []
        }
    
    def get_all_documents(self) -> Dict:
        """获取所有文档"""
        results = self.collection.get()
        return {
            'documents': results['documents'] if results['documents'] else [],
            'metadatas': results['metadatas'] if results['metadatas'] else [],
            'ids': results['ids'] if results['ids'] else []
        }
    
    def delete_documents(self, ids: List[str]):
        """删除指定文档"""
        self.collection.delete(ids=ids)
    
    def clear_collection(self):
        """清空集合"""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.ef
            )
        except Exception:
            pass
