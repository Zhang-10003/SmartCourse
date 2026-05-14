import requests
import json
import sys
import os
from typing import List, Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from setting import LLM_API_KEY

class DashScopeEmbedding:
    """使用阿里云 DashScope Embedding API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or LLM_API_KEY
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"
    
    def embed_text(self, text: str) -> List[float]:
        """
        将单个文本转换为向量
        
        Args:
            text: 输入文本
            
        Returns:
            向量列表
        """
        result = self.embed_batch([text])
        return result[0] if result else []
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        批量将文本转换为向量
        
        Args:
            texts: 文本列表
            
        Returns:
            向量列表
        """
        if not texts:
            return []
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "text-embedding-v3",
            "input": {"texts": texts}
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("output") and result["output"].get("embeddings"):
                embeddings = []
                for item in result["output"]["embeddings"]:
                    embeddings.append(item["embedding"])
                return embeddings
            else:
                print(f"Embedding API 返回格式异常: {result}")
                return [[] for _ in texts]
                
        except Exception as e:
            print(f"Embedding API 调用失败: {e}")
            return [[] for _ in texts]
    
    def compute_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        计算两个向量的余弦相似度
        
        Args:
            vec1: 向量1
            vec2: 向量2
            
        Returns:
            相似度 [0, 1]
        """
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)

