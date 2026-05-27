import json
import asyncio
from openai import OpenAI
from sqlalchemy import select, insert
from models import Question, Submission, StudentAnswer, AssignmentReport
from models.question import VALID_QUESTION_TYPES
from models import AsyncSessionFactory
from setting import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME

_report_generation_status: dict[int, str] = {}


def mark_report_generating(assignment_id: int):
    _report_generation_status[assignment_id] = "generating"


def get_report_generation_status(assignment_id: int) -> str | None:
    return _report_generation_status.get(assignment_id)


REPORT_PROMPT_TEMPLATE = """你是一名资深教学数据分析助手。请基于一份作业的全部题目、标准答案、评分结果和所有学生提交，生成供教师查看的"整份作业学情分析报告"。

你的任务不是逐题批改，而是识别每道题对应的知识点，统计各知识点的学生错误率，合并同义知识点，并总结班级整体学习表现与后续教学建议。

## 作业题目数据

{questions_json}

## 学生作答与判分数据

{answers_json}

## 核心规则

1. 每一道题都必须归属到一个明确的知识点。
   - 知识点应概括该题实际考查的核心概念或能力。
   - 不要直接复制题目标题。
   - 例如：题目考查 TCP 建连过程，可归纳为"TCP 三次握手机制"；题目考查循环边界，可归纳为"循环边界控制"。

2. 每个知识点的错误率按"答错该知识点的学生人数 / 已提交学生总人数"计算。
   - 例如：共有 10 名学生提交，其中 6 名学生答错了考查"TCP 三次握手机制"的题目，则该知识点错误率为 0.6，即 60%。
   - error_rate 必须为 0 到 1 之间的小数，保留最多两位小数。

3. 如果多道题考查的是含义相同或高度相近的知识点，必须合并为一个知识点。
   - 例如："TCP 三次握手步骤混淆"与"TCP 建连过程理解错误"应合并为"TCP 三次握手机制"。
   - 例如："循环终止条件写错"与"循环边界判断失误"应合并为"循环边界控制"。

4. 合并知识点后的错误率计算规则：
   - 若一个知识点对应多道题，只要某名学生在其中任意一道题上答错，该学生就计入该知识点的错误人数。
   - 同一名学生即使在该知识点对应的多道题上都答错，也只能计入一次。
   - affected_submission_ids 必须返回该知识点下答错学生的真实 submission_id，并去重。

5. 仅将错误率大于 0 的知识点放入 error_points。
   - 按 error_rate 从高到低排序。
   - 最多返回错误率最高的 4 个知识点。
   - 如果不足 4 个，则返回实际存在的错误知识点。
   - 如果所有学生全部答对，则返回空数组。

6. feedback_summary 必须是一段完整、连贯的中文总结，不使用编号或项目符号。
   - 内容应概括整体作答情况、错误率最高的知识点、学生普遍存在的理解问题，以及教师下一步应重点关注的方向。
   - 如果没有错误，应说明整体掌握良好，并给出进一步巩固或拓展方向。

7. teaching_advice 必须恰好返回 3 条建议。
   - keyword 为简短教学策略关键词，建议 2 至 6 个汉字，例如"动画演示"、"对比辨析"、"变式训练"。
   - text 为具体、可执行的教学建议，必须针对本次作业暴露出的错误知识点。
   - 如果没有错误，则给出巩固、迁移或拓展型建议。

8. 不要虚构题目、学生、提交 ID 或错误情况，只能根据输入数据分析。

9. 必须输出严格合法的 JSON，不要输出 Markdown 代码块、解释文字或 JSON 之外的任何内容。

## 输出格式

{{
  "error_points": [
    {{
      "name": "错误知识点名称",
      "affected_submission_ids": [1, 2, 3],
      "affected_count": 3,
      "error_rate": 0.6
    }}
  ],
  "feedback_summary": "一段完整的班级整体学情分析总结文本。",
  "teaching_advice": [
    {{
      "keyword": "动画演示",
      "text": "针对主要错误知识点给出的具体教学建议。"
    }},
    {{
      "keyword": "对比辨析",
      "text": "针对易混概念设计的具体教学建议。"
    }},
    {{
      "keyword": "变式训练",
      "text": "针对迁移应用与巩固提升的具体教学建议。"
    }}
  ]
}}"""


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
    mark_report_generating(assignment_id)
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
                _report_generation_status[assignment_id] = "error"
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
                _report_generation_status[assignment_id] = "error"
                return

            # 写入库 - 新格式直接保存 LLM 返回的完整结果
            report_data = json.dumps(llm_result, ensure_ascii=False)

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
            _report_generation_status[assignment_id] = "ready"
            print(f"[REPORT_GEN] ✅ 报告已生成并写入 DB", flush=True)

    except Exception as e:
        _report_generation_status[assignment_id] = "error"
        print(f"[REPORT_GEN] ❌ 异常: {e}", flush=True)
        import traceback
        traceback.print_exc()
