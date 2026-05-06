from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base


class Assignment(Base):
    """作业模型"""
    __tablename__ = "assignments"
    
    assignment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_title = Column(String(200), nullable=False)
    deadline = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="ongoing")
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    
    teacher = relationship("User", back_populates="assignments")
    questions = relationship("Question", back_populates="assignment")
    submissions = relationship("Submission", back_populates="assignment")
    shares = relationship("AssignmentShare", back_populates="assignment")
    student_assignments = relationship("StudentAssignment", back_populates="assignment")