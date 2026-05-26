from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


VALID_QUESTION_TYPES = (
    "choice",
    "multiple_choice",
    "true_false",
    "code_fill",
    "fill_blank",
    "matching",
    "short_answer",
)


class Question(Base):
    """题目模型"""
    __tablename__ = "questions"
    
    question_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"), nullable=False, index=True)
    type = Column(String(30), nullable=False, index=True)
    question_title = Column(String(500), nullable=False)
    options = Column(Text)
    content = Column(Text)
    code = Column(Text)
    fields = Column(Text)
    left_items = Column(Text)
    right_items = Column(Text)
    correct_answers = Column(Text)
    is_multiple = Column(Boolean, nullable=False, default=False)
    analysis = Column(Text)
    score = Column(Integer, nullable=False, default=10)
    sort_order = Column(Integer, nullable=False, default=0)
    
    assignment = relationship("Assignment", back_populates="questions")
    student_answers = relationship("StudentAnswer", back_populates="question")
