from sqlalchemy import Column, Integer, String

from . import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)  # 明文密码，不需要哈希
    user_type = Column(Integer, nullable=False)  # 用户类型
