from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from . import Base


class AssignmentReport(Base):
    __tablename__ = "assignment_reports"

    report_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"), nullable=False, index=True, unique=True)
    report_data = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    assignment = relationship("Assignment", backref="report")
