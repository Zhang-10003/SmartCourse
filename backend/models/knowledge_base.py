from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.sql import func

from . import Base


class KnowledgeBase(Base):
    """知识库文件模型"""
    __tablename__ = "knowledge_base"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    teacher_id = Column(Integer, default=1, index=True)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False, index=True)
    file_size = Column(BigInteger, nullable=False)
    file_path = Column(String(500), nullable=False)
    status = Column(Integer, default=0)
    upload_time = Column(DateTime, default=func.now())
    embedding_status = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<KnowledgeBase(id={self.id}, file_name={self.file_name}, file_type={self.file_type})>"
