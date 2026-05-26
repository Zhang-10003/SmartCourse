from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models import Assignment, Question, AssignmentShare, User, Student, StudentAssignment, Submission, StudentAnswer, AssignmentReport
from models.question import VALID_QUESTION_TYPES
from dependencies import get_session
from schemas.assignment import (
    AssignmentCreate, 
    AssignmentResponse, 
    QuestionCreate, 
    QuestionResponse,
    ShareCreate,
    ShareResponse,
    SubmitRequest,
    AnswerItem
)
from datetime import datetime
import uuid
import json
import asyncio
from typing import Dict, Any
from services.ai_grader import grade_submission
from services.report_generator import generate_report

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

        question_type = question_data.get('type', '')
        if question_type not in VALID_QUESTION_TYPES:
            return {"success": False, "message": "不支持的题型"}
        
        new_question = Question(
            assignment_id=question_data.get('assignment_id', 0),
            type=question_type,
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
            result = await session.execute(
                select(Question).where(
                    Question.assignment_id == assignment_id,
                    Question.type.in_(VALID_QUESTION_TYPES)
                )
            )
        else:
            result = await session.execute(
                select(Question).where(Question.type.in_(VALID_QUESTION_TYPES))
            )
        
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
        questions_result = await session.execute(
            select(Question).where(
                Question.assignment_id == share.assignment_id,
                Question.type.in_(VALID_QUESTION_TYPES)
            ).order_by(Question.sort_order)
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
            select(Question).where(
                Question.assignment_id == assignment_id,
                Question.type.in_(VALID_QUESTION_TYPES)
            ).order_by(Question.sort_order)
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
        today_list = []
        recent_list = []
        today_date = now.date()

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
            
            created_date = assignment.created_at
            if isinstance(created_date, str):
                from datetime import datetime as dt
                try:
                    created_date = dt.fromisoformat(created_date.replace('Z', '+00:00'))
                except:
                    pass

            assignment_data = {
                "assignment_id": assignment.assignment_id,
                "title": assignment.assignment_title,
                "deadline": deadline.strftime("截止: %m-%d %H:%M") if hasattr(deadline, 'strftime') else "截止: " + str(assignment.deadline),
                "deadline_ts": int(deadline.timestamp()) if hasattr(deadline, 'timestamp') else 0,
                "status": status,
                "share_code": share_code,
                "created_at": assignment.created_at.isoformat() if hasattr(assignment.created_at, 'isoformat') else str(assignment.created_at)
            }

            if hasattr(created_date, 'date') and created_date.date() == today_date:
                today_list.append(assignment_data)
            else:
                recent_list.append(assignment_data)

            print(f"作业: {assignment.assignment_title}, deadline: {deadline}, status: {status}, share_code: {share_code}")

        return {
            "success": True, 
            "data": {
                "today": today_list,
                "recent": recent_list
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

        # 查询该学生已有的提交记录
        submission_result = await session.execute(
            select(Submission.submission_id, Submission.assignment_id).where(
                Submission.student_id == student_id,
                Submission.assignment_id.in_(assignment_ids) if assignment_ids else False
            )
        )
        submitted_ids = {row.assignment_id for row in submission_result.all()}

        for assignment in assignments:
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
            elif assignment.assignment_id in submitted_ids:
                status = "submitted"
                status_text = "已提交"
            else:
                status = "processing"
                status_text = "进行中"

            result.append({
                "assignment_id": assignment.assignment_id,
                "title": assignment.assignment_title,
                "deadline": deadline.strftime("%m-%d %H:%M") if hasattr(deadline, 'strftime') else str(assignment.deadline),
                "deadline_ts": int(deadline.timestamp()) if hasattr(deadline, 'timestamp') else 0,
                "statusType": status,
                "statusText": status_text
            })

        # 排序：进行中 → 已提交 → 已截止
        status_priority = {"processing": 0, "submitted": 1, "expired": 2}
        result.sort(key=lambda x: (status_priority.get(x["statusType"], 99), x.get("deadline", "")))

        print(f"返回 {len(result)} 个作业数据")
        return {"success": True, "data": result}

    except Exception as e:
        import traceback
        print(f"获取作业列表失败: {str(e)}")
        print(traceback.format_exc())
        return {"success": False, "message": f"获取作业列表失败: {str(e)}"}


@router.post("/submit", response_model=dict)
async def submit_assignment(
    req: SubmitRequest,
    session: AsyncSession = Depends(get_session)
):
    """学生提交作业"""
    try:
        print(f"学生 {req.student_id} 提交作业 {req.assignment_id}")

        # 1. 检查是否已提交
        existing = await session.execute(
            select(Submission).where(
                Submission.assignment_id == req.assignment_id,
                Submission.student_id == req.student_id
            )
        )
        if existing.scalar_one_or_none():
            return {"success": False, "message": "已提交过该作业"}

        # 2. 获取所有题目
        questions_result = await session.execute(
            select(Question).where(
                Question.assignment_id == req.assignment_id,
                Question.type.in_(VALID_QUESTION_TYPES)
            )
        )
        questions = {q.question_id: q for q in questions_result.scalars().all()}

        # 3. 创建提交记录 - 初始状态设为批改中
        submission = Submission(
            assignment_id=req.assignment_id,
            student_id=req.student_id,
            submit_time=datetime.now(),
            status="grading"
        )
        session.add(submission)
        await session.flush()

        # 4. 逐题判分
        total_score = 0
        answer_records = []
        for ans in req.answers:
            question = questions.get(ans.question_id)
            if not question:
                continue

            correct = json.loads(question.correct_answers) if question.correct_answers else None
            user_ans = json.loads(ans.answer) if ans.answer else None
            is_correct, score = grade_answer(question.type, user_ans, correct, question.score)

            total_score += score
            answer_records.append({
                "submission_id": submission.submission_id,
                "question_id": ans.question_id,
                "answer": ans.answer,
                "is_correct": is_correct,
                "score": score
            })

        # 5. 批量插入答案
        await session.execute(
            StudentAnswer.__table__.insert(), answer_records
        )

        # 6. 暂不更新总分，等AI批改完成后再更新
        submission.total_score = None
        await session.commit()

        print(f"提交成功，进入AI批改流程")

        # 异步触发 AI 批改
        asyncio.create_task(grade_submission(submission.submission_id, total_score))

        return {
            "success": True,
            "data": {
                "submission_id": submission.submission_id,
                "total_score": None,
                "status": "grading"
            },
            "message": "提交成功"
        }

    except Exception as e:
        await session.rollback()
        import traceback
        print(f"提交作业失败: {str(e)}")
        print(traceback.format_exc())
        return {"success": False, "message": f"提交失败: {str(e)}"}


@router.get("/submit/{assignment_id}/{student_id}", response_model=dict)
async def get_submission(
    assignment_id: int,
    student_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取学生某作业的提交记录和答案"""
    try:
        sub_result = await session.execute(
            select(Submission).where(
                Submission.assignment_id == assignment_id,
                Submission.student_id == student_id
            )
        )
        submission = sub_result.scalar_one_or_none()
        if not submission:
            return {"success": False, "message": "未提交"}

        ans_result = await session.execute(
            select(StudentAnswer).where(StudentAnswer.submission_id == submission.submission_id)
        )
        answers = ans_result.scalars().all()

        return {
            "success": True,
            "data": {
                "submission_id": submission.submission_id,
                "submit_time": submission.submit_time.isoformat() if hasattr(submission.submit_time, 'isoformat') else str(submission.submit_time),
                "total_score": float(submission.total_score) if submission.total_score else 0,
                "feedback": submission.feedback or "",
                "answers": [
                    {
                        "question_id": a.question_id,
                        "answer": a.answer,
                        "is_correct": a.is_correct,
                        "score": float(a.score) if a.score else 0,
                        "feedback": a.feedback or ""
                    }
                    for a in answers
                ]
            }
        }
    except Exception as e:
        import traceback
        print(f"获取提交记录失败: {str(e)}")
        print(traceback.format_exc())
        return {"success": False, "message": f"获取提交记录失败: {str(e)}"}


def grade_answer(q_type, user_ans, correct_ans, full_score):
    """判分逻辑"""
    if user_ans is None or correct_ans is None:
        return False, 0

    if q_type == 'choice':
        if not isinstance(user_ans, list) or not isinstance(correct_ans, list):
            return False, 0
        if sorted(user_ans) == sorted(correct_ans):
            return True, full_score
        return False, 0

    elif q_type == 'true_false':
        return user_ans == correct_ans, full_score if user_ans == correct_ans else 0

    elif q_type == 'fill_blank':
        if not isinstance(user_ans, list) or not isinstance(correct_ans, list):
            return False, 0
        correct_count = 0
        for i, c in enumerate(correct_ans):
            if i < len(user_ans) and str(user_ans[i]).strip() == str(c).strip():
                correct_count += 1
        if correct_count == len(correct_ans):
            return True, full_score
        total_blank = max(len(correct_ans), len(user_ans))
        partial = int(full_score * correct_count / total_blank) if total_blank > 0 else 0
        return correct_count == total_blank, partial

    elif q_type == 'short_answer':
        return True, full_score

    elif q_type == 'matching':
        if not isinstance(user_ans, list) or not isinstance(correct_ans, list):
            return False, 0
        user_pairs = sorted((p.get('l'), p.get('r')) for p in user_ans)
        correct_pairs = sorted((p.get('l'), p.get('r')) for p in correct_ans)
        if user_pairs == correct_pairs:
            return True, full_score
        correct_matches = sum(1 for up in user_pairs if up in correct_pairs)
        total_pairs = len(correct_pairs)
        partial = int(full_score * correct_matches / total_pairs) if total_pairs > 0 else 0
        return correct_matches == total_pairs, partial

    elif q_type == 'code_fill':
        if not isinstance(user_ans, list) or not isinstance(correct_ans, list):
            return False, 0
        correct_count = 0
        for i, c in enumerate(correct_ans):
            if i < len(user_ans) and str(user_ans[i]).strip() == str(c).strip():
                correct_count += 1
        if correct_count == len(correct_ans):
            return True, full_score
        total_fields = max(len(correct_ans), len(user_ans))
        partial = int(full_score * correct_count / total_fields) if total_fields > 0 else 0
        return correct_count == total_fields, partial

    return False, 0


@router.post("/assignments/{assignment_id}/close", response_model=dict)
async def close_assignment(
    assignment_id: int,
    session: AsyncSession = Depends(get_session)
):
    """手动截止作业 + 异步生成报告"""
    try:
        result = await session.execute(
            select(Assignment).where(Assignment.assignment_id == assignment_id)
        )
        assignment = result.scalar_one_or_none()
        if not assignment:
            return {"success": False, "message": "作业不存在"}

        assignment.status = "closed"
        await session.commit()

        asyncio.create_task(generate_report(assignment_id))

        print(f"作业 {assignment_id} 已截止，异步生成报告中...")
        return {"success": True, "message": "作业已截止，报告生成中"}

    except Exception as e:
        await session.rollback()
        print(f"截止作业失败: {e}")
        return {"success": False, "message": f"截止失败: {str(e)}"}


@router.get("/assignments/{assignment_id}/report", response_model=dict)
async def get_assignment_report(
    assignment_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取作业报告"""
    try:
        result = await session.execute(
            select(AssignmentReport).where(AssignmentReport.assignment_id == assignment_id)
        )
        report = result.scalar_one_or_none()
        if not report:
            return {"success": False, "message": "报告尚未生成"}

        return {
            "success": True,
            "data": {
                "report_id": report.report_id,
                "assignment_id": report.assignment_id,
                "report_data": json.loads(report.report_data),
                "created_at": report.created_at.isoformat() if hasattr(report.created_at, 'isoformat') else str(report.created_at)
            }
        }
    except Exception as e:
        print(f"获取报告失败: {e}")
        return {"success": False, "message": f"获取报告失败: {str(e)}"}


@router.get("/assignments/{assignment_id}/stats", response_model=dict)
async def get_assignment_stats(
    assignment_id: int,
    session: AsyncSession = Depends(get_session)
):
    """获取作业实时统计数据"""
    try:
        # 1. 总人数（student_assignments + submissions 并集）
        sa_q = select(StudentAssignment.student_id).where(StudentAssignment.assignment_id == assignment_id)
        sub_q = select(Submission.student_id).where(Submission.assignment_id == assignment_id)
        union_q = sa_q.union(sub_q).subquery()
        total_result = await session.execute(select(func.count()).select_from(union_q))
        total_students = total_result.scalar() or 0

        # 2. 已提交人数
        sub_result = await session.execute(
            select(Submission).where(Submission.assignment_id == assignment_id)
        )
        submissions = sub_result.scalars().all()
        submitted_count = len(submissions)

        # 3. 总分（该作业所有题目的 score 之和）
        score_result = await session.execute(
            select(func.coalesce(func.sum(Question.score), 0))
            .where(
                Question.assignment_id == assignment_id,
                Question.type.in_(VALID_QUESTION_TYPES)
            )
        )
        total_score = float(score_result.scalar() or 0)

        # 4. 每题信息（用于柱状图）
        q_result = await session.execute(
            select(Question).where(
                Question.assignment_id == assignment_id,
                Question.type.in_(VALID_QUESTION_TYPES)
            ).order_by(Question.sort_order)
        )
        questions = q_result.scalars().all()

        submitted_ids = [s.submission_id for s in submissions]
        sub_student_ids = [s.student_id for s in submissions]

        # 5. 查询所有 student_answers
        all_answers = []
        if submitted_ids:
            a_result = await session.execute(
                select(StudentAnswer).where(StudentAnswer.submission_id.in_(submitted_ids))
            )
            all_answers = a_result.scalars().all()

        # 6. 每道题错误率
        question_scores = []
        hardest_q = {"label": "", "error_rate": 0}
        colors_pool = ["#6366f1", "#818cf8", "#a5b4fc", "#c7d2fe", "#6366f1", "#818cf8", "#a5b4fc", "#c7d2fe"]

        for i, q in enumerate(questions):
            q_answers = [a for a in all_answers if a.question_id == q.question_id]
            wrong_count = sum(1 for a in q_answers if a.is_correct is False)
            # 没有学生提交时，错误率设为-1，表示不显示或显示为"-"
            error_rate = wrong_count / submitted_count if submitted_count else -1
            question_scores.append({
                "label": f"Q{q.sort_order + 1}",
                "error_rate": round(error_rate, 2) if error_rate >= 0 else -1,
                "color": colors_pool[i % len(colors_pool)]
            })
            # 只在有错误率时才更新最难题目
            if error_rate >= 0 and error_rate > hardest_q["error_rate"]:
                hardest_q = {"label": f"Q{q.sort_order + 1}", "error_rate": round(error_rate, 2)}

        # 7. 成绩分布 + 平均分
        avg_score = 0
        excellent = good = pass_ = fail = 0
        for s in submissions:
            s_score = float(s.total_score) if s.total_score else 0
            pct = s_score / total_score if total_score else 0
            avg_score += s_score
            if pct >= 0.9: excellent += 1
            elif pct >= 0.75: good += 1
            elif pct >= 0.6: pass_ += 1
            else: fail += 1

        if submitted_count:
            avg_score = round(avg_score / submitted_count, 1)

        excellent_rate = f"{round(excellent / submitted_count * 100) if submitted_count else 0}%"

        # 8. 已提交学生列表
        submitted_students = []
        if sub_student_ids:
            stu_result = await session.execute(
                select(Student).where(Student.user_id.in_(sub_student_ids))
            )
            student_map = {s.user_id: s for s in stu_result.scalars().all()}

            for s in submissions:
                stu = student_map.get(s.student_id)
                name = stu.student_name if stu else f"学生{s.student_id}"
                submit_time = s.submit_time.strftime("%m-%d %H:%M") if hasattr(s.submit_time, 'strftime') else str(s.submit_time)
                
                # 根据状态决定显示什么
                if s.status == "grading":
                    status_text = "批改中"
                    score_text = "-"
                elif s.status == "graded":
                    status_text = "已批改"
                    score_text = str(float(s.total_score)) if s.total_score else "0"
                else:
                    status_text = "已提交"
                    score_text = str(float(s.total_score)) if s.total_score else "0"
                
                submitted_students.append({
                    "name": name,
                    "className": "",
                    "id": str(s.student_id),
                    "submit_time": submit_time,
                    "score": score_text,
                    "status": status_text
                })

        # 9. 未提交学生列表（同样取并集）
        sa_set = set()
        sa_r = await session.execute(
            select(StudentAssignment.student_id).where(StudentAssignment.assignment_id == assignment_id)
        )
        sa_set = {row[0] for row in sa_r.all()}
        sub_set = set(sub_student_ids)
        all_student_ids = sa_set | sub_set

        unsubmitted_ids = all_student_ids - sub_set
        unsubmitted_students = []
        if unsubmitted_ids:
            stu_result = await session.execute(
                select(Student).where(Student.user_id.in_(list(unsubmitted_ids)))
            )
            stu_map = {s.user_id: s for s in stu_result.scalars().all()}
            for uid in sorted(unsubmitted_ids):
                stu = stu_map.get(uid)
                name = stu.student_name if stu else f"学生{uid}"
                unsubmitted_students.append({
                    "name": name,
                    "className": "",
                    "id": str(uid)
                })

        return {
            "success": True,
            "data": {
                "total_students": total_students,
                "submitted_count": submitted_count,
                "avg_score": avg_score,
                "total_score": total_score,
                "excellent_rate": excellent_rate,
                "hardest_question": hardest_q,
                "score_distribution": {
                    "excellent": excellent,
                    "good": good,
                    "pass": pass_,
                    "fail": fail
                },
                "question_scores": question_scores,
                "submitted_students": submitted_students,
                "unsubmitted_students": unsubmitted_students
            }
        }

    except Exception as e:
        import traceback
        print(f"获取统计数据失败: {e}")
        traceback.print_exc()
        return {"success": False, "message": f"获取统计数据失败: {str(e)}"}
