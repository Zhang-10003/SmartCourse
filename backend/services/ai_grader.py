import json
import asyncio
import logging
from openai import OpenAI
from sqlalchemy import select, update
from models import Submission, StudentAnswer, Question
from models import AsyncSessionFactory
from setting import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME

logger = logging.getLogger('ai_grader')
logger.setLevel(logging.INFO)

GRADING_PROMPT_TEMPLATE = """你是一个专业的作业批改助手。你需要对学生的作业答案进行逐题批改，给出得分和详细的文字反馈。

## 输入数据格式

你会收到一个 JSON 对象，包含若干题目。每道题的字段如下：

| 字段 | 说明 |
|------|------|
| question_id | 题目ID |
| type | 题型：choice / multiple_choice / true_false / fill_blank / code_fill / matching / short_answer |
| question_title | 题目标题或题干 |
| options | 仅 choice / multiple_choice 有，选项文本数组 |
| content | 仅 fill_blank 有，含 ???? 作为空位的原文 |
| code | 仅 code_fill 有，含 ???? 的代码文本 |
| fields | 仅 code_fill 有，[{value, answer}, ...] |
| left_items | 仅 matching 有，左侧项文本数组 |
| right_items | 仅 matching 有，右侧项文本数组 |
| correct_answers | 标准答案的JSON字符串 |
| is_multiple | 仅多选题为 true |
| analysis | 教师提供的解析（可选） |
| score | 该题满分（整数） |
| user_answer | 学生答案的JSON字符串 |

## 各题型判分规则

### 1. 单选题 (choice)
- correct_answers: JSON数组如 "[0]"
- user_answer: JSON数组如 "[0]"
- user_answer[0] 与 correct_answers[0] 相等则满分，否则0分
- 反馈指出正确选项文本，参考analysis解析

### 2. 多选题 (multiple_choice)
- correct_answers: JSON数组如 "[0,1,3]"
- user_answer: JSON数组如 "[0,1]"
- 排序后逐元素比较，完全一致才给满分，否则0分（全对全错）
- 反馈指出漏选/多选的选项文本

### 3. 判断题 (true_false)
- correct_answers: 字符串 "true" 或 "false"，解析后为 boolean
- user_answer: 解析后为 boolean
- 相等则满分，否则0分
- 反馈解释正确答案

### 4. 填空题 (fill_blank)
- correct_answers: JSON字符串数组 ["答案1","答案2",...]
- user_answer: JSON字符串数组 ["学生填1","学生填2",...]
- content 中 ???? 的位置标明了每个空
- 判分步骤：
  a) 阅读 content，理解每个 ???? 在上下文中的含义
  b) 根据每个空的重要/难易程度，将满分分配到各个空（各空分值之和必须等于满分，可为带1位小数的数值）
  c) 逐空对比：trim去空格后忽略大小写比较
  d) 答对得该空分值，答错得0

### 5. 代码填空 (code_fill)
- correct_answers: JSON字符串数组
- user_answer: JSON字符串数组
- 判分同填空题，根据代码逻辑上下文中每个空的重要性分配分值
- 反馈结合代码上下文

### 6. 匹配题 (matching)
- left_items: 左侧项文本数组
- right_items: 右侧项文本数组
- correct_answers: [{"l":0,"r":0}, {"l":1,"r":1}, ...]
- user_answer: [{"l":0,"r":1}, {"l":1,"r":0}, ...]
- 判分步骤：
  a) 阅读每一对匹配的内容，判断该对的重要/难易程度
  b) 根据重要程度将满分分配到每一对（各对分值之和等于满分）
  c) 逐对比较 l 和 r 是否都正确
  d) 正确得该对分值，错误得0

### 7. 简答题 (short_answer)
- correct_answers: {"standardAnswer": "参考答案"}
- user_answer: 字符串
- 根据内容完整性（是否覆盖关键要点）、准确性（是否有错误）、表达清晰度综合评分，以20%为梯度（0% / 20% / 40% / 60% / 80% / 100%）
- 反馈要详细、有建设性

## 输出格式

必须返回严格的 JSON，不要包含 markdown 代码块标记：

{
  "results": [
    {
      "question_id": 1,
      "score": 10,
      "is_correct": true,
      "feedback": "回答正确！...\\n\\n解析：..."
    }
  ],
  "summary": {
    "total_score": 45,
    "max_score": 70,
    "error_summary": "总结本次作业的主要错误类型和共性问题，用一段中文说明",
    "study_suggestions": "给出有针对性的学习建议、复习方向或练习方法，用一段中文说明"
  }
}

## 字段要求
1. score 必须是数字，不能超过该题满分，可以是整数或保留1位小数
2. results[].feedback 用中文，包含是否正确、原因、正确内容、改进建议
3. summary.error_summary 概括本次作业的核心错误类型和共性问题（一段文字）
4. summary.study_suggestions 给出具体可操作的学习建议（一段文字）
5. analysis 字段不为空时可参考
6. 除了 "results" 和 "summary" 两个顶级字段，不要输出其他内容

## 待批改数据

{questions_json}"""


def call_llm(prompt: str) -> dict | None:
    """同步调用 LLM（在 asyncio.to_thread 中执行）"""
    try:
        client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
        response = client.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=4096
        )
        result = response.choices[0].message.content
        logger.info("LLM 返回: %s", result[:200])
        return json.loads(result)
    except Exception as e:
        logger.error("LLM 调用失败: %s", str(e))
        return None


async def grade_submission(submission_id: int):
    """后台异步批改：查询数据 → 调LLM → 写库"""
    print(f"[AI_GRADER] ===== 开始批改 submission_id={submission_id} =====", flush=True)
    try:
        async with AsyncSessionFactory() as session:
            print(f"[AI_GRADER] 1. session 创建成功", flush=True)

            sub_result = await session.execute(
                select(Submission).where(Submission.submission_id == submission_id)
            )
            submission = sub_result.scalar_one_or_none()
            if not submission:
                print(f"[AI_GRADER] ❌ submission {submission_id} 不存在", flush=True)
                return
            print(f"[AI_GRADER] 2. 查到 submission, assignment_id={submission.assignment_id}", flush=True)

            q_result = await session.execute(
                select(Question).where(Question.assignment_id == submission.assignment_id)
            )
            questions = q_result.scalars().all()
            print(f"[AI_GRADER] 3. 查到 {len(questions)} 道题", flush=True)

            a_result = await session.execute(
                select(StudentAnswer).where(StudentAnswer.submission_id == submission_id)
            )
            answers = a_result.scalars().all()
            answer_map = {a.question_id: a for a in answers}
            print(f"[AI_GRADER] 4. 查到 {len(answers)} 条学生答案", flush=True)

            questions_data = []
            for q in questions:
                sa = answer_map.get(q.question_id)
                questions_data.append({
                    "question_id": q.question_id,
                    "type": q.type,
                    "question_title": q.question_title,
                    "options": json.loads(q.options) if q.options else None,
                    "content": q.content,
                    "code": q.code,
                    "fields": json.loads(q.fields) if q.fields else None,
                    "left_items": json.loads(q.left_items) if q.left_items else None,
                    "right_items": json.loads(q.right_items) if q.right_items else None,
                    "correct_answers": q.correct_answers,
                    "is_multiple": q.is_multiple,
                    "analysis": q.analysis,
                    "score": q.score,
                    "user_answer": sa.answer if sa else None
                })

            print(f"[AI_GRADER] 5. 构造 LLM 请求体完成, 准备调LLM...", flush=True)

            prompt = GRADING_PROMPT_TEMPLATE.replace("{questions_json}", json.dumps(questions_data, ensure_ascii=False, indent=2))
            print(f"[AI_GRADER] 6. Prompt 长度={len(prompt)} 字符", flush=True)

            llm_result = await asyncio.to_thread(call_llm, prompt)
            print(f"[AI_GRADER] 7. LLM 返回: {str(llm_result)[:200]}", flush=True)
            if not llm_result:
                print(f"[AI_GRADER] ❌ LLM 批改无返回，跳过", flush=True)
                return

            results = llm_result.get("results", [])
            summary = llm_result.get("summary", {})
            print(f"[AI_GRADER] 8. 解析到 {len(results)} 条批改结果", flush=True)

            for r in results:
                qid = r.get("question_id")
                fb = r.get("feedback", "")
                sa = answer_map.get(qid)
                if sa:
                    await session.execute(
                        update(StudentAnswer)
                        .where(StudentAnswer.answer_id == sa.answer_id)
                        .values(feedback=fb)
                    )

            error_summary = summary.get("error_summary", "")
            study_suggestions = summary.get("study_suggestions", "")
            combined_feedback = ""
            if error_summary:
                combined_feedback += f"【错误总结】{error_summary}\n"
            if study_suggestions:
                combined_feedback += f"【学习建议】{study_suggestions}"
            if combined_feedback:
                await session.execute(
                    update(Submission)
                    .where(Submission.submission_id == submission_id)
                    .values(feedback=combined_feedback)
                )

            await session.commit()
            print(f"[AI_GRADER] ✅ 批改完成, 数据已写入 DB", flush=True)

    except Exception as e:
        print(f"[AI_GRADER] ❌ 异常: {e}", flush=True)
        import traceback
        traceback.print_exc()
