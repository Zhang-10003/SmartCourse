import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.rag_service import RAGService

def test_rag():
    print("=== 测试 RAG 模块 ===")
    
    # 初始化服务
    rag_service = RAGService(use_mock=True)
    print("1. RAG服务初始化成功")
    
    # 添加测试知识
    test_knowledge = [
        "Python是一种高级编程语言，由Guido van Rossum于1991年发布。",
        "Python支持多种编程范式，包括面向对象、函数式和过程式编程。",
        "Python的特点包括简洁的语法、强大的标准库和丰富的第三方库。",
        "常用的Python库包括numpy、pandas、scikit-learn和TensorFlow。",
        "Python广泛应用于Web开发、数据科学、人工智能等领域。"
    ]
    rag_service.add_knowledge(test_knowledge)
    print(f"2. 添加了 {len(test_knowledge)} 条知识到知识库")
    
    # 测试检索功能
    retrieved = rag_service.retrieve_knowledge("Python编程")
    print(f"3. 检索到 {len(retrieved['documents'])} 条相关知识")
    
    # 测试题目生成
    result = rag_service.generate_questions("Python编程", num_questions=3)
    print(f"4. 生成了 {len(result['questions'])} 道题目")
    
    # 打印题目
    print("\n=== 生成的题目 ===")
    for i, q in enumerate(result['questions']):
        print(f"\n题目 {i+1}:")
        print(f"  类型: {q['type']}")
        print(f"  内容: {q['question_title']}")
        if 'options' in q:
            print(f"  选项: {q['options']}")
        print(f"  答案: {q['correct_answers']}")
        print(f"  解析: {q['analysis']}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_rag()