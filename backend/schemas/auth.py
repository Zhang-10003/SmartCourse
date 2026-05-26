from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """登录响应模型"""
    user_id: int
    username: str
    user_type: int
    access_token: str
    student_name: Optional[str] = None
    student_no: Optional[str] = None
