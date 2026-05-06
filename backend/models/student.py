from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Student(Base):
    """学生模型"""
    __tablename__ = "students"
    
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True, index=True)
    student_name = Column(String(100), nullable=False)
    student_no = Column(String(50), unique=True, index=True, nullable=False)
    
    user = relationship("User", back_populates="student")