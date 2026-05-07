import json
import random

class QuestionGenerator:
    def __init__(self, use_mock=True, openai_api_key=None):
        """
        初始化题目生成器
        :param use_mock: 是否使用模拟模式
        :param openai_api_key: OpenAI API密钥（非模拟模式时需要）
        """
        self.use_mock = use_mock
        self.openai_api_key = openai_api_key
        
        if not use_mock and not openai_api_key:
            raise ValueError("非模拟模式需要提供OpenAI API密钥")
    
    def generate_questions(self, topic, knowledge, num_questions=5):
        """
        生成题目
        :param topic: 主题
        :param knowledge: 知识内容
        :param num_questions: 题目数量
        :return: 题目列表
        """
        if self.use_mock:
            return self._generate_mock_questions(topic, knowledge, num_questions)
        else:
            return self._generate_real_questions(topic, knowledge, num_questions)
    
    def _generate_mock_questions(self, topic, knowledge, num_questions):
        """模拟生成题目"""
        questions = []
        
        question_types = [
            {'type': 'choice', 'name': '单选题'},
            {'type': 'multiple_choice', 'name': '多选题'},
            {'type': 'true_false', 'name': '判断题'},
            {'type': 'fill_blank', 'name': '填空题'},
            {'type': 'short_answer', 'name': '简答题'}
        ]
        
        for i in range(num_questions):
            q_type = question_types[i % len(question_types)]
            
            if q_type['type'] == 'choice':
                questions.append({
                    'type': 'choice',
                    'question_title': f"{topic} - 单选题 {i+1}",
                    'options': ['选项A', '选项B', '选项C', '选项D'],
                    'correct_answers': [random.randint(0, 3)],
                    'analysis': '本题考查' + topic + '相关知识',
                    'score': 10
                })
            elif q_type['type'] == 'multiple_choice':
                questions.append({
                    'type': 'multiple_choice',
                    'question_title': f"{topic} - 多选题 {i+1}",
                    'options': ['选项A', '选项B', '选项C', '选项D'],
                    'correct_answers': [0, 1],
                    'analysis': '本题考查' + topic + '相关知识',
                    'score': 15
                })
            elif q_type['type'] == 'true_false':
                questions.append({
                    'type': 'true_false',
                    'question_title': f"{topic} - 判断题 {i+1}: 以下说法是否正确？",
                    'correct_answers': random.choice(['true', 'false']),
                    'analysis': '本题考查' + topic + '相关知识',
                    'score': 5
                })
            elif q_type['type'] == 'fill_blank':
                questions.append({
                    'type': 'fill_blank',
                    'question_title': f"{topic} - 填空题 {i+1}: 请填写答案：______",
                    'correct_answers': ['答案'],
                    'analysis': '本题考查' + topic + '相关知识',
                    'score': 10
                })
            elif q_type['type'] == 'short_answer':
                questions.append({
                    'type': 'short_answer',
                    'question_title': f"{topic} - 简答题 {i+1}: 请简述相关内容",
                    'correct_answers': {'standardAnswer': '参考答案...'},
                    'analysis': '本题考查' + topic + '相关知识',
                    'score': 20
                })
        
        return questions
    
    def _generate_real_questions(self, topic, knowledge, num_questions):
        """使用真实LLM生成题目"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_api_key)
            
            prompt = f"""
            根据以下知识内容，生成{num_questions}道高质量题目，返回JSON格式：
            
            主题：{topic}
            
            知识内容：
            {knowledge}
            
            要求：
            1. 题目类型：单选题、多选题、判断题、填空题、简答题
            2. 题目必须基于提供的知识
            3. 返回格式必须是JSON数组，包含：type(题型)、question_title(题目内容)、options(选项，选择题需要)、correct_answers(正确答案)、analysis(解析)、score(分值)
            4. 不要包含任何额外文本
            
            输出示例：
            [
                {{
                    "type": "choice",
                    "question_title": "题目内容",
                    "options": ["A", "B", "C", "D"],
                    "correct_answers": [0],
                    "analysis": "解析",
                    "score": 10
                }}
            ]
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            print(f"LLM调用失败: {str(e)}")
            return self._generate_mock_questions(topic, knowledge, num_questions)