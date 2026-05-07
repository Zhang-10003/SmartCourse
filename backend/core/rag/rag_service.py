from .vector_db import VectorDB
from .question_generator import QuestionGenerator

class RAGService:
    def __init__(self, use_mock=True, openai_api_key=None):
        """
        初始化RAG服务
        :param use_mock: 是否使用模拟模式
        :param openai_api_key: OpenAI API密钥（非模拟模式时需要）
        """
        self.vector_db = VectorDB()
        self.generator = QuestionGenerator(use_mock=use_mock, openai_api_key=openai_api_key)
    
    def add_knowledge(self, documents, metadatas=None):
        """
        添加知识到知识库
        :param documents: 文档内容列表
        :param metadatas: 元数据列表
        """
        self.vector_db.add_documents(documents, metadatas)
    
    def retrieve_knowledge(self, query, n_results=5):
        """
        检索相关知识
        :param query: 查询文本
        :param n_results: 返回结果数量
        :return: 检索到的知识
        """
        return self.vector_db.query(query, n_results)
    
    def generate_questions(self, topic, num_questions=5):
        """
        根据主题生成题目
        :param topic: 主题
        :param num_questions: 题目数量
        :return: 题目列表
        """
        # 1. 检索相关知识
        retrieved = self.retrieve_knowledge(topic, n_results=3)
        knowledge = "\n".join(retrieved['documents'])
        
        # 2. 生成题目
        questions = self.generator.generate_questions(topic, knowledge, num_questions)
        
        return {
            'questions': questions,
            'retrieved_knowledge': retrieved['documents']
        }
    
    def clear_knowledge(self):
        """清空知识库"""
        self.vector_db.clear_collection()
    
    def get_knowledge_count(self):
        """获取知识库文档数量"""
        result = self.vector_db.get_all_documents()
        return len(result['ids']) if result['ids'] else 0