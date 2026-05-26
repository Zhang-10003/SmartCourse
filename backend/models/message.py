from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"), nullable=False, index=True)
    content = Column(String(500), nullable=False)
    type = Column(String(20), nullable=False, default="assignment_deadline")
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
