from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Teacher(Base):
    """教师模型"""
    __tablename__ = "teachers"
    
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True, index=True)
    teacher_name = Column(String(100), nullable=False)
    teacher_no = Column(String(50), unique=True, index=True, nullable=False)
    
    user = relationship("User", back_populates="teacher")