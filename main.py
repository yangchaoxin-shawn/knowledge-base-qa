"""
[FILE]: main.py
[ROLE]: 主程序入口，控制启动流程和交互逻辑（流式输出）
[DEPS]: Python Standard Library | @kb_manager.py, @modules/interaction_manager.py, @config/settings.py
[VIBE_LOGIC]:
- 核心逻辑：演示问答 → 交互流程选择（y/n）→ 索引管理（a/b）→ 交互模式（支持超时）
- 关键约束：演示问题列表固定为 5 个，支持 y/n 和 a/b 输入验证，5分钟超时退出
"""

import sys
import time
from kb_manager import KnowledgeBaseManager
from modules.interaction_manager import InteractionManager
from config.settings import DEMO_QUESTIONS


def run_demo(kb):
    """运行演示问答"""
    print("\n【演示问答阶段】")
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


def main():
    """主程序入口"""
    print("=" * 60)
    print("       企业知识库问答系统 v1.0")
    print("=" * 60)
    
    try:
        kb = KnowledgeBaseManager(load_existing=True)
        
        run_demo(kb)
        
        interaction_manager = InteractionManager(kb)
        interaction_manager.start_post_demo_flow()
        
    except Exception as e:
        print(f"\n❌ 程序启动失败: {str(e)}")
        with open("./logs/error.log", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 启动错误: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()