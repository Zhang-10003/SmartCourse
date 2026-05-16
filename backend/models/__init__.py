from sqlalchemy.ext.asyncio import create_async_engine
from setting import DATABASE_URL

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionFactory = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=True
)

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix":'ix_%(column_0_label)s',
        "uq":'uq_%(table_name)s_%(column_0_name)s',
        "ck":'ck_%(table_name)s_%(constraint_name)s',
        "fk":'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        "pk":'pk_%(table_name)s',
    })

from .user import User
from .teacher import Teacher
from .student import Student
from .assignment import Assignment
from .assignment_share import AssignmentShare
from .question import Question
from .submission import Submission
from .student_assignment import StudentAssignment
from .student_answer import StudentAnswer
from .knowledge_base import KnowledgeBase
__all__ = ['engine', 'AsyncSessionFactory', 'Base', 'User', 'Teacher', 'Student', 'Assignment', 'AssignmentShare', 'Question', 'Submission', 'StudentAssignment', 'StudentAnswer', 'KnowledgeBase']