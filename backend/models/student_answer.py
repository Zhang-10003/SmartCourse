from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship

from . import Base


class StudentAnswer(Base):
    """学生答题模型"""
    __tablename__ = "student_answers"
    
    answer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submission_id = Column(Integer, ForeignKey("submissions.submission_id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"), nullable=False, index=True)
    answer = Column(String(1000))
    is_correct = Column(Boolean)
    score = Column(DECIMAL(5, 2))
    
    submission = relationship("Submission", back_populates="student_answers")
    question = relationship("Question", back_populates="student_answers")