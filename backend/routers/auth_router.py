from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from dependencies import get_session
from schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
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
    
    return LoginResponse(
        user_id=user.user_id,
        username=user.username,
        user_type=user.user_type,
        access_token=access_token
    )