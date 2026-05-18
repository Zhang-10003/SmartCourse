from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Assignment, Question, AssignmentShare, User, StudentAssignment
from dependencies import get_session
from schemas.assignment import (
    AssignmentCreate, 
    AssignmentResponse, 
    QuestionCreate, 
    QuestionResponse,
    ShareCreate,
    ShareResponse
)
from datetime import datetime
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
        
        # 获取作业详情
        assignment_result = await session.execute(select(Assignment).where(Assignment.assignment_id == share.assignment_id))
        assignment = assignment_result.scalar_one_or_none()
        
        # 获取题目列表
        questions_result = await session.execute(select(Question).where(Question.assignment_id == share.assignment_id).order_by(Question.sort_order))
        questions = questions_result.scalars().all()
        
        question_list = []
        for question in questions:
            question_list.append({
                "question_id": question.question_id,
                "type": question.type,
                "question_title": question.question_title,
                "options": question.options,
                "content": question.content,
                "code": question.code,
                "fields": question.fields,
                "left_items": question.left_items,
                "right_items": question.right_items,
                "is_multiple": question.is_multiple,
                "analysis": question.analysis,
                "score": question.score,
                "sort_order": question.sort_order
            })
        
        return {
            "success": True,
            "data": {
                "share_id": share.share_id,
                "share_code": share.share_code,
                "access_type": share.access_type,
                "assignment": {
                    "assignment_id": assignment.assignment_id,
                    "assignment_title": assignment.assignment_title,
                    "deadline": assignment.deadline.isoformat() if hasattr(assignment.deadline, 'isoformat') else str(assignment.deadline),
                    "status": assignment.status,
                    "created_at": assignment.created_at.isoformat() if hasattr(assignment.created_at, 'isoformat') else str(assignment.created_at)
                },
                "questions": question_list
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e), "message": "获取分享链接失败"}


@router.post("/student/share/{share_code}", response_model=dict)
async def student_access_share(
    share_code: str,
    student_id: int,
    session: AsyncSession = Depends(get_session)
):
    """学生通过分享链接获取作业"""
    try:
        print(f"学生 {student_id} 正在通过分享码 {share_code} 获取作业...")
        
        # 1. 查找分享链接
        share_result = await session.execute(
            select(AssignmentShare).where(AssignmentShare.share_code == share_code)
        )
        share = share_result.scalar_one_or_none()
        
        if not share:
            print(f"分享码 {share_code} 不存在")
            return {"success": False, "message": "分享链接不存在或已失效"}
        
        assignment_id = share.assignment_id
        print(f"找到作业ID: {assignment_id}")
        
        # 2. 检查学生是否已关联此作业
        existing_result = await session.execute(
            select(StudentAssignment).where(
                StudentAssignment.student_id == student_id,
                StudentAssignment.assignment_id == assignment_id
            )
        )
        existing = existing_result.scalar_one_or_none()
        
        if existing:
            print("学生已关联此作业")
        else:
            # 新建关联
            new_association = StudentAssignment(
                student_id=student_id,
                assignment_id=assignment_id,
                source="share",
                added_at=datetime.now()
            )
            session.add(new_association)
            await session.commit()
            print("已创建新的关联")
        
        # 3. 获取作业详情
        assignment_result = await session.execute(
            select(Assignment).where(Assignment.assignment_id == assignment_id)
        )
        assignment = assignment_result.scalar_one_or_none()
        
        # 4. 获取题目列表
        questions_result = await session.execute(
            select(Question).where(Question.assignment_id == assignment_id).order_by(Question.sort_order)
        )
        questions = questions_result.scalars().all()
        
        question_list = []
        for question in questions:
            question_list.append({
                "question_id": question.question_id,
                "type": question.type,
                "question_title": question.question_title,
                "options": question.options,
                "content": question.content,
                "code": question.code,
                "fields": question.fields,
                "left_items": question.left_items,
                "right_items": question.right_items,
                "is_multiple": question.is_multiple,
                "analysis": question.analysis,
                "score": question.score,
                "sort_order": question.sort_order
            })
        
        print(f"返回作业: {assignment.assignment_title}, 题目数: {len(question_list)}")
        return {
            "success": True,
            "data": {
                "assignment_id": assignment.assignment_id,
                "assignment_title": assignment.assignment_title,
                "deadline": assignment.deadline.isoformat() if hasattr(assignment.deadline, 'isoformat') else str(assignment.deadline),
                "status": assignment.status,
                "questions": question_list
            },
            "message": "作业获取成功"
        }
        
    except Exception as e:
        await session.rollback()
        import traceback
        print(f"获取作业失败: {str(e)}")
        print(traceback.format_exc())
        return {"success": False, "message": f"获取作业失败: {str(e)}"}


@router.get("/teacher/{teacher_id}/assignments", response_model=dict)
async def get_teacher_assignments(
    teacher_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取教师的所有作业列表"""
    try:
        print(f"正在获取教师 {teacher_id} 的作业列表...")
        
        # 先查询所有作业，调试用
        all_assignments_result = await session.execute(
            select(Assignment)
        )
        all_assignments = all_assignments_result.scalars().all()
        print(f"数据库中共有 {len(all_assignments)} 个作业")
        for a in all_assignments:
            print(f"  - id: {a.assignment_id}, title: {a.assignment_title}, user_id: {a.user_id}")
        
        # 获取该教师的作业，如果没有就返回所有作业（调试模式）
        assignments_result = await session.execute(
            select(Assignment).where(Assignment.user_id == teacher_id).order_by(Assignment.created_at.desc())
        )
        assignments = assignments_result.scalars().all()
        
        if len(assignments) == 0:
            print(f"教师 {teacher_id} 没有作业，返回所有作业用于调试")
            assignments = all_assignments
        
        print(f"返回 {len(assignments)} 个作业")

        # 构造返回数据 - 简化逻辑，直接返回所有作业到 today
        result = []
        now = datetime.now()
        
        # 先处理作业数据
        assignment_with_deadline = []
        for assignment in assignments:
            # 判断作业状态
            status = "进行中"

            deadline = assignment.deadline
            if isinstance(deadline, str):
                from datetime import datetime as dt
                try:
                    deadline = dt.fromisoformat(deadline.replace('Z', '+00:00'))
                except:
                    pass

            if deadline and now > deadline:
                status = "已截止"
            
            # 保存原始的 deadline 用于排序
            assignment_with_deadline.append({
                "assignment": assignment,
                "deadline_date": deadline,
                "status": status
            })
        
        # 按截止时间降序排列（截止时间晚的在前面）
        assignment_with_deadline.sort(key=lambda x: x["deadline_date"] if x["deadline_date"] else datetime.min, reverse=True)
        
        # 构造最终返回数据
        for item in assignment_with_deadline:
            assignment = item["assignment"]
            deadline = item["deadline_date"]
            status = item["status"]
            
            # 查询该作业的 share_code
            share_code = None
            try:
                share_result = await session.execute(
                    select(AssignmentShare).where(AssignmentShare.assignment_id == assignment.assignment_id)
                )
                share = share_result.scalar_one_or_none()
                if share:
                    share_code = share.share_code
            except Exception as e:
                print(f"查询 share_code 失败: {e}")
            
            assignment_data = {
                "assignment_id": assignment.assignment_id,
                "title": assignment.assignment_title,
                "deadline": deadline.strftime("截止: %m-%d %H:%M") if hasattr(deadline, 'strftime') else "截止: " + str(assignment.deadline),
                "status": status,
                "share_code": share_code,
                "created_at": assignment.created_at.isoformat() if hasattr(assignment.created_at, 'isoformat') else str(assignment.created_at)
            }
            result.append(assignment_data)
            print(f"作业: {assignment.assignment_title}, deadline: {deadline}, status: {status}, share_code: {share_code}")

        return {
            "success": True, 
            "data": {
                "today": result,
                "recent": []
            }
        }

    except Exception as e:
        print(f"获取作业列表失败: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return {"success": False, "message": f"获取作业列表失败: {str(e)}"}


@router.get("/student/{student_id}/assignments", response_model=dict)
async def get_student_assignments(
    student_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取学生的所有作业列表"""
    try:
        print(f"正在获取学生 {student_id} 的作业列表...")
        
        # 获取学生关联的所有作业（通过分享链接添加的）
        assoc_result = await session.execute(
            select(StudentAssignment).where(StudentAssignment.student_id == student_id)
        )
        associations = assoc_result.scalars().all()

        assignment_ids = [assoc.assignment_id for assoc in associations]
        print(f"找到 {len(assignment_ids)} 个关联的作业")

        # 获取作业详情
        if not assignment_ids:
            print("学生没有通过分享链接添加的作业")
            return {"success": True, "data": []}
        else:
            assignments_result = await session.execute(
                select(Assignment).where(Assignment.assignment_id.in_(assignment_ids))
            )
            assignments = assignments_result.scalars().all()

        print(f"找到 {len(assignments)} 个作业")

        # 构造返回数据
        result = []
        now = datetime.now()

        for assignment in assignments:
            # 判断作业状态
            status = "processing"
            status_text = "进行中"

            deadline = assignment.deadline
            if isinstance(deadline, str):
                from datetime import datetime as dt
                try:
                    deadline = dt.fromisoformat(deadline.replace('Z', '+00:00'))
                except:
                    pass

            if deadline and now > deadline:
                status = "expired"
                status_text = "已截止"

            result.append({
                "assignment_id": assignment.assignment_id,
                "title": assignment.assignment_title,
                "deadline": deadline.strftime("%m-%d %H:%M") if hasattr(deadline, 'strftime') else str(assignment.deadline),
                "statusType": status,
                "statusText": status_text
            })

        print(f"返回 {len(result)} 个作业数据")
        return {"success": True, "data": result}

    except Exception as e:
        import traceback
        print(f"获取作业列表失败: {str(e)}")
        print(traceback.format_exc())
        return {"success": False, "message": f"获取作业列表失败: {str(e)}"}