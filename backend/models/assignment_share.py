from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base


class AssignmentShare(Base):
    """作业分享模型"""
    __tablename__ = "assignment_shares"
    
    share_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"), nullable=False, index=True)
    share_code = Column(String(64), unique=True, nullable=False, index=True)
    access_type = Column(String(20), nullable=False, default="submit")
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    
    assignment = relationship("Assignment", back_populates="shares")