from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base


class Submission(Base):
    """作业提交模型"""
    __tablename__ = "submissions"
    
    submission_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    submit_time = Column(DateTime, nullable=False, default=datetime.now)
    status = Column(String(20), nullable=False, default="submitted")
    total_score = Column(DECIMAL(5, 2))
    feedback = Column(Text)
    
    assignment = relationship("Assignment", back_populates="submissions")
    student_answers = relationship("StudentAnswer", back_populates="submission")