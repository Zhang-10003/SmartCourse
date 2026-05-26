from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User, Student
from dependencies import get_session
from schemas import LoginRequest, LoginResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=dict)
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(User).where(User.username == login_data.username))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    if user.password != login_data.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    access_token = f"token_{user.user_id}"
    
    response_data = {
        "user_id": user.user_id,
        "username": user.username,
        "user_type": user.user_type,
        "access_token": access_token
    }
    
    print(f"登录用户: user_id={user.user_id}, username={user.username}, user_type={user.user_type}")
    
    # 如果是学生，还需要查询学生信息
    if user.user_type == 1:
        student_result = await session.execute(select(Student).where(Student.user_id == user.user_id))
        student = student_result.scalar_one_or_none()
        print(f"查询学生信息: student={student}")
        if student:
            response_data["student_name"] = student.student_name
            response_data["student_no"] = student.student_no
            print(f"添加学生信息: student_name={student.student_name}, student_no={student.student_no}")
    
    print(f"返回登录响应: {response_data}")
    return response_data