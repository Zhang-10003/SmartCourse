from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Assignment, Question, AssignmentShare, User
from dependencies import get_session
from schemas.assignment import (
    AssignmentCreate, 
    AssignmentResponse, 
    QuestionCreate, 
    QuestionResponse,
    ShareCreate,
    ShareResponse
)
import uuid
from typing import Dict, Any

router = APIRouter(prefix="/api", tags=["assignments"])


@router.post("/assignments", response_model=dict)
async def create_assignment(
    assignment: AssignmentCreate,
    session: AsyncSession = Depends(get_session)
):
    try:
        new_assignment = Assignment(
            assignment_title=assignment.assignment_title,
            deadline=assignment.deadline,
            status=assignment.status,
            user_id=1
        )
        session.add(new_assignment)
        await session.commit()
        await session.refresh(new_assignment)
        
        return {
            "success": True,
            "data": {
                "assignment_id": new_assignment.assignment_id,
                "assignment_title": new_assignment.assignment_title,
                "deadline": new_assignment.deadline.isoformat() if hasattr(new_assignment.deadline, 'isoformat') else str(new_assignment.deadline),
                "status": new_assignment.status,
                "user_id": new_assignment.user_id,
                "created_at": new_assignment.created_at.isoformat() if hasattr(new_assignment.created_at, 'isoformat') else str(new_assignment.created_at)
            }
        }
    except Exception as e:
        await session.rollback()
        return {"success": False, "error": str(e), "message": "创建作业失败"}


@router.post("/questions", response_model=dict)
async def create_question(
    question_data: Dict[str, Any],
    session: AsyncSession = Depends(get_session)
):
    try:
        print("接收到的题目数据:", question_data)
        
        new_question = Question(
            assignment_id=question_data.get('assignment_id', 0),
            type=question_data.get('type', ''),
            question_title=question_data.get('question_title', ''),
            options=question_data.get('options'),
            content=question_data.get('content'),
            code=question_data.get('code'),
            fields=question_data.get('fields'),
            left_items=question_data.get('left_items'),
            right_items=question_data.get('right_items'),
            correct_answers=question_data.get('correct_answers'),
            is_multiple=question_data.get('is_multiple', False),
            analysis=question_data.get('analysis', ''),
            score=question_data.get('score', 10),
            sort_order=question_data.get('sort_order', 0)
        )
        session.add(new_question)
        await session.commit()
        await session.refresh(new_question)
        
        return {
            "success": True,
            "data": {
                "question_id": new_question.question_id,
                "assignment_id": new_question.assignment_id,
                "type": new_question.type
            }
        }
    except Exception as e:
        await session.rollback()
        print("创建题目错误:", str(e))
        return {"success": False, "error": str(e), "message": "创建题目失败"}


@router.post("/shares", response_model=dict)
async def create_share(
    share: ShareCreate,
    session: AsyncSession = Depends(get_session)
):
    try:
        share_code = str(uuid.uuid4()).replace('-', '')[:16]
        
        new_share = AssignmentShare(
            assignment_id=share.assignment_id,
            share_code=share_code,
            access_type=share.access_type,
            created_by=1
        )
        session.add(new_share)
        await session.commit()
        await session.refresh(new_share)
        
        return {
            "success": True,
            "data": {
                "share_id": new_share.share_id,
                "assignment_id": new_share.assignment_id,
                "share_code": new_share.share_code,
                "access_type": new_share.access_type,
                "created_by": new_share.created_by,
                "created_at": new_share.created_at.isoformat() if hasattr(new_share.created_at, 'isoformat') else str(new_share.created_at)
            }
        }
    except Exception as e:
        await session.rollback()
        return {"success": False, "error": str(e), "message": "生成分享链接失败"}


@router.get("/assignments", response_model=dict)
async def get_assignments(
    session: AsyncSession = Depends(get_session)
):
    try:
        result = await session.execute(select(Assignment))
        assignments = result.scalars().all()
        
        assignment_list = []
        for assignment in assignments:
            assignment_list.append({
                "assignment_id": assignment.assignment_id,
                "assignment_title": assignment.assignment_title,
                "deadline": assignment.deadline.isoformat() if hasattr(assignment.deadline, 'isoformat') else str(assignment.deadline),
                "status": assignment.status,
                "user_id": assignment.user_id,
                "created_at": assignment.created_at.isoformat() if hasattr(assignment.created_at, 'isoformat') else str(assignment.created_at)
            })
        
        return {"success": True, "data": assignment_list}
    except Exception as e:
        return {"success": False, "error": str(e), "message": "获取作业列表失败"}


@router.get("/questions", response_model=dict)
async def get_questions(
    assignment_id: int = None,
    session: AsyncSession = Depends(get_session)
):
    try:
        if assignment_id:
            result = await session.execute(select(Question).where(Question.assignment_id == assignment_id))
        else:
            result = await session.execute(select(Question))
        
        questions = result.scalars().all()
        
        question_list = []
        for question in questions:
            question_list.append({
                "question_id": question.question_id,
                "assignment_id": question.assignment_id,
                "type": question.type,
                "question_title": question.question_title,
                "options": question.options,
                "content": question.content,
                "code": question.code,
                "fields": question.fields,
                "left_items": question.left_items,
                "right_items": question.right_items,
                "correct_answers": question.correct_answers,
                "is_multiple": question.is_multiple,
                "analysis": question.analysis,
                "score": question.score,
                "sort_order": question.sort_order
            })
        
        return {"success": True, "data": question_list}
    except Exception as e:
        return {"success": False, "error": str(e), "message": "获取题目列表失败"}


@router.get("/shares/{share_code}", response_model=dict)
async def get_share_by_code(
    share_code: str,
    session: AsyncSession = Depends(get_session)
):
    try:
        result = await session.execute(select(AssignmentShare).where(AssignmentShare.share_code == share_code))
        share = result.scalar_one_or_none()
        
        if not share:
            return {"success": False, "error": "NotFound", "message": "分享链接不存在"}
        
        return {
            "success": True,
            "data": {
                "share_id": share.share_id,
                "assignment_id": share.assignment_id,
                "share_code": share.share_code,
                "access_type": share.access_type,
                "created_by": share.created_by,
                "created_at": share.created_at.isoformat() if hasattr(share.created_at, 'isoformat') else str(share.created_at)
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": "获取分享链接失败"}