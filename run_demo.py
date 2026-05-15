"""
[FILE]: run_demo.py
[ROLE]: 演示模式脚本，快速执行内置问题的问答演示（流式输出）
[DEPS]: Python Standard Library | @kb_manager.py, @config/settings.py
[VIBE_LOGIC]:
- 核心逻辑：初始化知识库（加载现有索引），遍历演示问题列表执行流式问答
- 关键约束：默认加载已有索引，使用 settings.py 中的 DEMO_QUESTIONS，流式输出答案
"""

import sys
from kb_manager import KnowledgeBaseManager
from config.settings import DEMO_QUESTIONS


def run_demo():
    """运行演示模式"""
    print("=" * 60)
    print("       企业知识库问答系统 - 演示模式")
    print("=" * 60)
    
    kb = KnowledgeBaseManager(load_existing=True)
    
    print("\n【演示问答】")
    print("-" * 30)
    
    for question in DEMO_QUESTIONS:
        print(f"问题：{question}")
        print()
        print("答案：", end='', flush=True)
        
        for chunk in kb.ask_stream(question):
            if not isinstance(chunk, list):
                print(chunk, end='', flush=True)
                sys.stdout.flush()
        
        print()
        print("-" * 50)
    
    stats = kb.get_stats()
    print(f"\n知识库统计：文档数={stats['doc_count']}，日志数={stats['log_count']}")


if __name__ == "__main__":
    run_demo()