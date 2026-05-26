import json
import asyncio
from openai import OpenAI
from sqlalchemy import select, insert
from models import Question, Submission, StudentAnswer, AssignmentReport
from models.question import VALID_QUESTION_TYPES
from models import AsyncSessionFactory
from setting import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME

REPORT_PROMPT_TEMPLATE = """你是一个教学数据分析助手。以下是一份作业的答题数据，请分析学生的整体掌握情况。

## 作业题目

{questions_json}

## 学生答案汇总

{answers_json}

请分析这份作业并输出 JSON（不要包含任何额外文字或 markdown 标记）：

{{
  "total_submitted": 提交人数（整数）,
  "total_students": 该作业学生总数（整数，提交人数+未提交人数）,
  "knowledge_points": [
    {{
      "name": "知识点名称",
      "error_rate": 错误人数/提交人数（0~1的小数,保留2位小数）,
      "mistake_types": [
        {{"description": "错误类型描述", "count": 人数（整数）, "percent": 0~1的小数 }}
      ]
    }}
  ]
}}

要求：
1. 根据题目内容、标准答案和学生的实际回答，推断本题涉及的知识点
2. 把相同意思但表述不同的答案归为同一类错误类型
3. knowledge_points 按 error_rate 从高到低排序
4. mistake_types 按 count 从高到低排序
5. 错误类型描述应简洁准确"""


def call_llm(prompt: str) -> dict | None:
    try:
        client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
        response = client.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=4096
        )
        result = response.choices[0].message.content
        print(f"[REPORT_GEN] LLM 返回: {result[:300]}", flush=True)
        return json.loads(result)
    except Exception as e:
        print(f"[REPORT_GEN] LLM 调用失败: {e}", flush=True)
        return None


async def generate_report(assignment_id: int):
    print(f"[REPORT_GEN] ===== 开始生成报告 assignment_id={assignment_id} =====", flush=True)
    try:
        async with AsyncSessionFactory() as session:
            # 查所有题目
            q_result = await session.execute(
                select(Question).where(
                    Question.assignment_id == assignment_id,
                    Question.type.in_(VALID_QUESTION_TYPES)
                ).order_by(Question.sort_order)
            )
            questions = q_result.scalars().all()
            print(f"[REPORT_GEN] 查到 {len(questions)} 道题", flush=True)

            # 查所有提交
            sub_result = await session.execute(
                select(Submission).where(Submission.assignment_id == assignment_id)
            )
            submissions = sub_result.scalars().all()
            print(f"[REPORT_GEN] 查到 {len(submissions)} 条提交", flush=True)

            submission_ids = [s.submission_id for s in submissions]
            if not submission_ids or not questions:
                print(f"[REPORT_GEN] 无数据，跳过", flush=True)
                return

            # 查所有答案
            a_result = await session.execute(
                select(StudentAnswer).where(StudentAnswer.submission_id.in_(submission_ids))
            )
            all_answers = a_result.scalars().all()
            print(f"[REPORT_GEN] 查到 {len(all_answers)} 条答案", flush=True)

            # 构造 LLM 请求
            questions_data = []
            for q in questions:
                questions_data.append({
                    "question_id": q.question_id,
                    "type": q.type,
                    "question_title": q.question_title,
                    "options": json.loads(q.options) if q.options else None,
                    "content": q.content,
                    "code": q.code,
                    "left_items": json.loads(q.left_items) if q.left_items else None,
                    "right_items": json.loads(q.right_items) if q.right_items else None,
                    "correct_answers": q.correct_answers,
                    "is_multiple": q.is_multiple,
                    "analysis": q.analysis,
                    "score": q.score
                })

            # 按题目组织学生答案
            answers_by_q = {}
            valid_question_ids = {q.question_id for q in questions}
            for a in all_answers:
                qid = a.question_id
                if qid not in valid_question_ids:
                    continue
                if qid not in answers_by_q:
                    answers_by_q[qid] = []
                user_val = json.loads(a.answer) if a.answer else ""
                answers_by_q[qid].append({
                    "student_id": a.submission_id,
                    "answer": user_val,
                    "is_correct": a.is_correct,
                    "score": float(a.score) if a.score else 0
                })

            prompt = REPORT_PROMPT_TEMPLATE.replace("{questions_json}", json.dumps(questions_data, ensure_ascii=False, indent=2))
            prompt = prompt.replace("{answers_json}", json.dumps(answers_by_q, ensure_ascii=False, indent=2, default=str))

            print(f"[REPORT_GEN] Prompt 长度={len(prompt)} 字符", flush=True)

            llm_result = await asyncio.to_thread(call_llm, prompt)
            if not llm_result:
                print(f"[REPORT_GEN] LLM 无返回，跳过", flush=True)
                return

            # 写入库
            total_students = llm_result.get("total_students", 0)
            total_submitted = llm_result.get("total_submitted", len(submissions))
            kps = llm_result.get("knowledge_points", [])

            report_data = json.dumps({
                "total_submitted": total_submitted,
                "total_students": total_students,
                "knowledge_points": kps
            }, ensure_ascii=False)

            # UPSERT
            existing = await session.execute(
                select(AssignmentReport).where(AssignmentReport.assignment_id == assignment_id)
            )
            if existing.scalar_one_or_none():
                await session.execute(
                    AssignmentReport.__table__.update()
                    .where(AssignmentReport.assignment_id == assignment_id)
                    .values(report_data=report_data)
                )
            else:
                session.add(AssignmentReport(
                    assignment_id=assignment_id,
                    report_data=report_data
                ))

            await session.commit()
            print(f"[REPORT_GEN] ✅ 报告已生成并写入 DB", flush=True)

    except Exception as e:
        print(f"[REPORT_GEN] ❌ 异常: {e}", flush=True)
        import traceback
        traceback.print_exc()
