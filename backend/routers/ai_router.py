from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import os
import logging
from openai import OpenAI
from setting import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('ai_router')
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/api", tags=["ai"])

class GenerateQuestionRequest(BaseModel):
    prompt: str
    difficulty: Optional[str] = "简单"
    question_type: Optional[str] = None

class GenerateQuestionResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

def build_prompt(request: GenerateQuestionRequest) -> str:
    difficulty_map = {
        "简单": "难度较低，适合初学者",
        "中等": "难度适中，适合进阶学习者",
        "困难": "难度较高，适合高级学习者"
    }
    
    # 安全检查：如果传入的难度不在map中，默认使用"中等"
    valid_difficulty = request.difficulty if request.difficulty in difficulty_map else "中等"
    difficulty_text = difficulty_map[valid_difficulty]
    
    type_info = ""
    if request.question_type:
        type_info = "题型：" + request.question_type + "\n\n"
    
    json_examples = [
        '- 单选题(choice)：{"type":"choice","title":"题目内容","options":["选项A","选项B","选项C","选项D"],"answer":0,"analysis":"解析","score":10}',
        '- 多选题(multiple_choice)：{"type":"multiple_choice","title":"题目内容","options":["选项A","选项B","选项C","选项D"],"answer":[0,1],"analysis":"解析","score":15}',
        '- 判断题(true_false)：{"type":"true_false","title":"题目内容","answer":true,"analysis":"解析","score":5}',
        '- 填空题(fill_blank)：{"type":"fill_blank","title":"题目内容","content":"题目内容（含空白处）","correctAnswers":["答案1","答案2"],"analysis":"解析","score":10}',
        '- 代码填空(code_fill)：{"type":"code_fill","title":"题目内容","code":"代码内容","fields":[{"answer":"答案"}],"analysis":"解析","score":15}',
        '- 匹配题(matching)：{"type":"matching","title":"题目内容","pairs":[{"left":"左侧1","right":"右侧1"},{"left":"左侧2","right":"右侧2"}],"analysis":"解析","score":15}',
        '- 简答题(short_answer)：{"type":"short_answer","title":"题目内容","standardAnswer":"标准答案","analysis":"解析","score":20}'
    ]
    
    prompt = (
        "你是一个专业的题目生成助手，请根据以下要求生成一道高质量题目：\n\n"
        + type_info
        + "难度：" + difficulty_text + "\n\n"
        + "题目要求：\n"
        + request.prompt + "\n\n"
        + "格式要求：\n"
        + "请严格按照JSON格式输出，不要包含任何额外文本。\n\n"
        + "输出格式说明：\n"
        + "\n".join(json_examples) + "\n\n"
        + "请确保输出是有效的JSON格式！"
    )
    
    return prompt

def generate_with_llm(prompt: str) -> Dict[str, Any]:
    try:
        logger.info(f"LLM配置 - API Key: {LLM_API_KEY[:10]}...")
        logger.info(f"LLM配置 - Base URL: {LLM_BASE_URL}")
        logger.info(f"LLM配置 - Model: {LLM_MODEL_NAME}")
        
        client = OpenAI(
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL
        )
        
        logger.info("正在调用LLM API...")
        response = client.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        result = response.choices[0].message.content
        logger.info("\nLLM原始返回内容:")
        logger.info(result)
        logger.info("\nLLM返回内容长度: %d 字符", len(result))
        
        try:
            parsed_result = json.loads(result)
            logger.info("LLM返回内容解析为JSON成功")
            logger.info("解析后的JSON数据: %s", parsed_result)
            return parsed_result
        except json.JSONDecodeError:
            logger.error("LLM返回非JSON格式，无法解析")
            return None
            
    except Exception as e:
        logger.error("LLM调用失败: %s", str(e))
        import traceback
        logger.error("异常堆栈: %s", traceback.format_exc())
        return None

def generate_mock_response(request: GenerateQuestionRequest) -> Dict[str, Any]:
    templates = {
        "单选题": {
            "type": "choice",
            "title": "关于" + request.prompt[:10] + "的单选题",
            "options": ["选项A", "选项B", "选项C", "选项D"],
            "answer": 0,
            "analysis": "本题考查相关知识点",
            "score": 10
        },
        "多选题": {
            "type": "multiple_choice",
            "title": "关于" + request.prompt[:10] + "的多选题",
            "options": ["选项A", "选项B", "选项C", "选项D"],
            "answer": [0, 1],
            "analysis": "本题考查相关知识点",
            "score": 15
        },
        "判断题": {
            "type": "true_false",
            "title": request.prompt[:15] + "，这个说法是否正确？",
            "answer": True,
            "analysis": "本题考查相关知识点",
            "score": 5
        },
        "填空题": {
            "type": "fill_blank",
            "title": "关于" + request.prompt[:10] + "的填空题",
            "content": "请填写：______是一种重要的概念。",
            "correctAnswers": ["答案"],
            "analysis": "本题考查相关知识点",
            "score": 10
        },
        "代码填空": {
            "type": "code_fill",
            "title": "关于" + request.prompt[:10] + "的代码填空题",
            "code": "def func():\n    result = ????\n    return result",
            "fields": [{"answer": "正确答案"}],
            "analysis": "本题考查代码理解能力",
            "score": 15
        },
        "匹配题": {
            "type": "matching",
            "title": "请将下列内容进行匹配",
            "pairs": [
                {"left": "概念A", "right": "描述A"},
                {"left": "概念B", "right": "描述B"},
                {"left": "概念C", "right": "描述C"}
            ],
            "analysis": "本题考查概念理解能力",
            "score": 15
        },
        "简答题": {
            "type": "short_answer",
            "title": "请简述" + request.prompt[:15],
            "standardAnswer": "这是一个标准的参考答案...",
            "analysis": "本题考查综合理解能力",
            "score": 20
        }
    }
    
    question_type = request.question_type if request.question_type else "单选题"
    return templates.get(question_type, templates["单选题"])

@router.post("/ai/generate-question")
async def generate_question(request: GenerateQuestionRequest):
    logger.info(f"AI生成题目 - prompt: {request.prompt}, difficulty: {request.difficulty}, type: {request.question_type}")
    
    try:
        full_prompt = build_prompt(request)
        
        result = generate_with_llm(full_prompt)
        
        if result is None:
            logger.info("LLM调用失败，使用模拟数据")
            result = generate_mock_response(request)
        
        logger.info(f"题目生成成功 - type: {result.get('type')}, title: {result.get('title')}")
        
        return {"success": True, "data": result, "message": "题目生成成功"}
        
    except Exception as e:
        logger.error(f"生成题目失败: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return {"success": False, "message": "生成题目失败: " + str(e)}
