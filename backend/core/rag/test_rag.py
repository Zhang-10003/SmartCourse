import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.embedding import DashScopeEmbedding
from rag.vector_db import VectorDB

def test_embedding():
    """测试 Embedding 功能"""
    print("=" * 60)
    print("测试 1: DashScope Embedding")
    print("=" * 60)
    
    embedding = DashScopeEmbedding()
    
    texts = [
        "Python编程语言",
        "Java编程语言",
        "计算机网络",
        "TCP/IP协议"
    ]
    
    print(f"\n输入文本: {texts}")
    
    embeddings = embedding.embed_batch(texts)
    
    print(f"\n生成了 {len(embeddings)} 个向量")
    print(f"每个向量维度: {len(embeddings[0]) if embeddings else 0}")
    
    # 测试相似度
    print("\n计算相似度:")
    sim1 = embedding.compute_similarity(embeddings[0], embeddings[1])  # Python vs Java
    sim2 = embedding.compute_similarity(embeddings[0], embeddings[2])  # Python vs 网络
    print(f"  Python vs Java: {sim1:.4f}")
    print(f"  Python vs 网络: {sim2:.4f}")


def test_vector_db():
    """测试向量数据库（ChromaDB）"""
    print("\n" + "=" * 60)
    print("测试 2: ChromaDB 向量数据库")
    print("=" * 60)
    
    db = VectorDB(collection_name="test_kb")
    
    # 添加测试知识
    test_documents = [
        "计算机网络：TCP/IP协议是互联网的基础协议，包括TCP和IP两个部分。",
        "TCP协议：传输控制协议，提供可靠的、面向连接的服务。",
        "IP协议：网际协议，负责数据包的路由和寻址。",
        "HTTP协议：超文本传输协议，用于Web浏览器和服务器之间的通信。",
        "Python编程：Python是一种高级编程语言，语法简洁易懂。",
        "机器学习：机器学习是人工智能的一个分支，让计算机从数据中学习。"
    ]
    
    test_metadatas = [
        {"category": "网络", "difficulty": "基础"},
        {"category": "网络", "difficulty": "基础"},
        {"category": "网络", "difficulty": "基础"},
        {"category": "网络", "difficulty": "进阶"},
        {"category": "编程", "difficulty": "基础"},
        {"category": "AI", "difficulty": "进阶"}
    ]
    
    print(f"\n添加 {len(test_documents)} 条文档...")
    db.add_documents(test_documents, metadatas=test_metadatas)
    
    # 测试查询
    queries = ["TCP协议", "Python", "人工智能"]
    
    for query in queries:
        print(f"\n查询: '{query}'")
        results = db.query(query, n_results=3)
        
        print(f"  找到 {len(results['documents'])} 条相关文档:")
        for i, (doc, meta, dist) in enumerate(zip(results['documents'], results['metadatas'], results['distances'])):
            print(f"    [{i+1}] (距离: {dist:.4f}) {meta.get('category', '')} - {doc[:50]}...")
    
    # 清理测试数据
    db.clear_collection()
    print("\n测试完成，已清理测试数据")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("RAG 模块测试 (ChromaDB)")
    print("=" * 60)
    
    # 测试 Embedding
    test_embedding()
    
    # 测试向量数据库
    test_vector_db()
    
    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)
