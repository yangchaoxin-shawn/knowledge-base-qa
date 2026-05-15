"""
[FILE]: utils/helpers.py
[ROLE]: 辅助函数模块，提供打印格式化、知识库初始化等通用工具
[DEPS]: os | @kb_manager.py
[VIBE_LOGIC]:
- 核心逻辑：print_answer 格式化输出问答结果，init_kb 处理索引选择逻辑
- 关键约束：打印格式为"问题：xxx\n答案：xxx\n来源：xxx"，支持 y/n 选择加载/重建索引
"""

import os


def print_answer(question, answer, sources):
    """
    格式化打印问答结果
    
    Args:
        question: 用户问题
        answer: 生成的答案
        sources: 来源文档标题列表
    """
    print(f"问题：{question}")
    print(f"答案：{answer}")
    if sources:
        print(f"来源：{', '.join(sources)}")
    print("-" * 50)


def init_kb(persist_dir="./data/faiss_index"):
    """
    初始化知识库，处理索引选择逻辑
    
    Args:
        persist_dir: FAISS 索引持久化目录（默认 ./data/faiss_index）
    
    Returns:
        KnowledgeBaseManager 实例
    """
    # 延迟导入避免循环依赖
    from kb_manager import KnowledgeBaseManager
    
    choice = input("是否加载已有 FAISS 索引？(y/n): ").strip().lower()
    
    if choice == 'y':
        if os.path.exists(persist_dir) and os.listdir(persist_dir):
            print("正在加载已有索引...")
            kb = KnowledgeBaseManager(persist_dir=persist_dir, load_existing=True)
            print("索引加载成功！")
        else:
            print("未找到已有索引，将重新创建...")
            kb = KnowledgeBaseManager(persist_dir=persist_dir, load_existing=False)
    else:
        print("正在重新创建索引...")
        kb = KnowledgeBaseManager(persist_dir=persist_dir, load_existing=False)
    
    return kb


def validate_input(prompt, valid_options=None):
    """
    验证用户输入
    
    Args:
        prompt: 提示信息
        valid_options: 有效选项列表（可选）
    
    Returns:
        str: 用户输入
    """
    while True:
        user_input = input(prompt).strip()
        
        if not user_input:
            print("请输入有效内容")
            continue
        
        if valid_options and user_input.lower() not in valid_options:
            print(f"请输入有效选项: {', '.join(valid_options)}")
            continue
        
        return user_input