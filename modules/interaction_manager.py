"""
[FILE]: modules/interaction_manager.py
[ROLE]: 用户交互流程管理模块，处理演示结束后的交互模式选择和索引管理
[DEPS]: os, sys, time, threading | @kb_manager.py
[VIBE_LOGIC]:
- 核心逻辑：实现演示结束后的交互流程，包括模式选择、索引管理、超时处理
- 关键约束：支持 y/n 和 a/b 输入验证，实现进度条和超时机制
"""

import os
import sys
import time
import threading


class InteractionManager:
    """
    用户交互流程管理器
    
    负责演示结束后的交互流程，包括模式选择、索引管理和超时处理。
    """
    
    def __init__(self, kb_manager):
        """
        初始化交互管理器
        
        Args:
            kb_manager: KnowledgeBaseManager 实例
        """
        self.kb_manager = kb_manager
        self.timeout_event = threading.Event()
        self.timeout_thread = None
        self.TIMEOUT_SECONDS = 300  # 5分钟超时
    
    def _start_timeout_timer(self):
        """启动超时定时器"""
        def timeout_callback():
            time.sleep(self.TIMEOUT_SECONDS)
            if not self.timeout_event.is_set():
                print("\n\n[超时提醒] 长时间无操作，即将退出交互模式...")
                time.sleep(2)
                self.timeout_event.set()
        
        self.timeout_thread = threading.Thread(target=timeout_callback, daemon=True)
        self.timeout_thread.start()
    
    def _reset_timeout_timer(self):
        """重置超时定时器"""
        self.timeout_event.set()
        time.sleep(0.1)
        self.timeout_event.clear()
        self._start_timeout_timer()
    
    def _show_progress_bar(self, current, total, prefix="", suffix=""):
        """
        显示进度条
        
        Args:
            current: 当前进度
            total: 总进度
            prefix: 前缀文本
            suffix: 后缀文本
        """
        bar_length = 20
        percent = (current / total) * 100
        filled_length = int(bar_length * current // total)
        bar = "=" * filled_length + " " * (bar_length - filled_length)
        sys.stdout.write(f"\r{prefix}[{bar}] {percent:.1f}% {suffix}")
        sys.stdout.flush()
    
    def _validate_input(self, prompt, valid_options, error_msg, case_insensitive=True):
        """
        验证用户输入
        
        Args:
            prompt: 提示信息
            valid_options: 有效选项列表
            error_msg: 错误提示信息
            case_insensitive: 是否忽略大小写
        
        Returns:
            str: 用户输入（已转换为小写，如果启用忽略大小写）
        """
        while True:
            user_input = input(prompt).strip()
            
            if case_insensitive:
                user_input = user_input.lower()
            
            if user_input in valid_options:
                return user_input
            
            print(f"❌ {error_msg}")
    
    def _rebuild_index_with_progress(self):
        """带进度条的索引重构"""
        print("\n🔄 开始执行全量索引重构，请稍候...")
        
        start_time = time.time()
        
        docs = []
        try:
            from data.simulated_docs import SIMULATED_DOCS
            docs = SIMULATED_DOCS
        except Exception as e:
            print(f"❌ 加载文档失败: {str(e)}")
            return False
        
        total_docs = len(docs)
        processed_docs = 0
        
        try:
            self.kb_manager.clear_kb()
            
            for i, doc in enumerate(docs, 1):
                self.kb_manager.add_document(
                    title=doc['title'],
                    content=doc['content'],
                    doc_id=doc['id']
                )
                processed_docs = i
                self._show_progress_bar(i, total_docs, prefix="构建进度:", suffix=f"({i}/{total_docs})")
                time.sleep(0.1)
            
            self._show_progress_bar(total_docs, total_docs, prefix="构建进度:", suffix="(完成)")
            print()
            
            elapsed_time = time.time() - start_time
            
            print(f"\n✅ 全量索引重构已完成，共处理 {processed_docs} 个文档，耗时 {elapsed_time:.2f} 秒")
            return True
        
        except Exception as e:
            print(f"\n❌ 索引重构失败: {str(e)}")
            import traceback
            with open("./logs/error.log", "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 索引重构错误: {traceback.format_exc()}\n")
            return False
    
    def _load_existing_index(self):
        """加载现有索引"""
        print("\n📂 已加载现有索引，正在进入交互模式...")
        
        try:
            success = self.kb_manager.load_index()
            
            if not success:
                print("⚠️  索引加载失败，尝试重建...")
                return self._rebuild_index_with_progress()
            
            doc_count = self.kb_manager.get_stats()['doc_count']
            print(f"✅ 索引加载成功，共 {doc_count} 个文档")
            return True
        
        except Exception as e:
            print(f"❌ 索引加载失败: {str(e)}")
            import traceback
            with open("./logs/error.log", "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 索引加载错误: {traceback.format_exc()}\n")
            return False
    
    def _handle_index_choice(self):
        """处理索引选择"""
        print("\n" + "=" * 50)
        print("请选择索引使用方式：")
        print("a) 使用已有的索引")
        print("b) 重新构建索引（全量重构）")
        print("=" * 50)
        
        choice = self._validate_input(
            "请输入选择(a/b): ",
            ['a', 'b'],
            "输入无效，请重新输入(a/b)"
        )
        
        if choice == 'a':
            return self._load_existing_index()
        else:
            return self._rebuild_index_with_progress()
    
    def _chat_interaction(self):
        """交互模式主循环"""
        print("\n" + "=" * 50)
        print("【交互模式】")
        print("输入 q 或 exit 退出程序")
        print("=" * 50)
        
        self._start_timeout_timer()
        
        while not self.timeout_event.is_set():
            try:
                user_input = input("\n> ").strip()
                
                self._reset_timeout_timer()
                
                if user_input.lower() in ['q', 'exit']:
                    print("👋 感谢使用，再见！")
                    break
                
                if not user_input:
                    continue
                
                print(f"\n问题：{user_input}")
                print()
                print("答案：", end='', flush=True)
                
                for chunk in self.kb_manager.ask_stream(user_input):
                    if not isinstance(chunk, list):
                        print(chunk, end='', flush=True)
                        sys.stdout.flush()
                
                print()
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n\n👋 感谢使用，再见！")
                break
            except Exception as e:
                print(f"\n❌ 处理请求时发生错误: {str(e)}")
                import traceback
                with open("./logs/error.log", "a", encoding="utf-8") as f:
                    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 交互错误: {traceback.format_exc()}\n")
    
    def start_post_demo_flow(self):
        """
        启动演示结束后的交互流程
        
        Returns:
            bool: 是否成功进入交互模式
        """
        print("\n" + "=" * 60)
        print("【演示结束】")
        print("=" * 60)
        
        choice = self._validate_input(
            "演示已结束，是否进入交互模式？(y/n): ",
            ['y', 'n'],
            "输入无效，请重新输入(y/n)"
        )
        
        if choice == 'n':
            print("👋 已退出交互模式，感谢使用")
            return False
        
        if not self._handle_index_choice():
            print("❌ 无法进入交互模式，程序退出")
            return False
        
        print("\n🚀 正在进入交互模式...")
        self._chat_interaction()
        return True