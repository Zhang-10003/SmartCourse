from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base


class StudentAssignment(Base):
    """学生作业关联模型"""
    __tablename__ = "student_assignments"
    
    sa_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"), nullable=False, index=True)
    source = Column(String(20), nullable=False, default="share")
    added_at = Column(DateTime, nullable=False, default=datetime.now)
    
    assignment = relationship("Assignment", back_populates="student_assignments")