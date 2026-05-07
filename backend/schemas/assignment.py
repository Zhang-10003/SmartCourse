from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AssignmentCreate(BaseModel):
    """创建作业请求模型"""
    assignment_title: str
    deadline: str
    status: str = "ongoing"


class AssignmentResponse(BaseModel):
    """作业响应模型"""
    assignment_id: int
    assignment_title: str
    deadline: str
    status: str
    user_id: int
    created_at: datetime


class QuestionCreate(BaseModel):
    """创建题目请求模型"""
    assignment_id: int
    type: str
    question_title: str
    options: Optional[str] = Field(None)
    content: Optional[str] = Field(None)
    code: Optional[str] = Field(None)
    fields: Optional[str] = Field(None)
    left_items: Optional[str] = Field(None)
    right_items: Optional[str] = Field(None)
    correct_answers: Optional[str] = Field(None)
    is_multiple: bool = False
    analysis: str = ""
    score: int = 10
    sort_order: int = 0


class QuestionResponse(BaseModel):
    """题目响应模型"""
    question_id: int
    assignment_id: int
    type: str
    question_title: str
    options: Optional[str] = None
    content: Optional[str] = None
    code: Optional[str] = None
    fields: Optional[str] = None
    left_items: Optional[str] = None
    right_items: Optional[str] = None
    correct_answers: Optional[str] = None
    is_multiple: bool
    analysis: str
    score: int
    sort_order: int


class ShareCreate(BaseModel):
    """创建分享请求模型"""
    assignment_id: int
    access_type: str = "submit"


class ShareResponse(BaseModel):
    """分享响应模型"""
    share_id: int
    assignment_id: int
    share_code: str
    access_type: str
    created_by: int
    created_at: datetime


class SuccessResponse(BaseModel):
    """成功响应模型"""
    success: bool = True
    message: str = "操作成功"


class ErrorResponse(BaseModel):
    """错误响应模型"""
    success: bool = False
    error: str
    message: str