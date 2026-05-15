"""
[FILE]: test_interaction.py
[ROLE]: 交互流程测试脚本
[DEPS]: unittest, unittest.mock | @interaction_manager.py, @kb_manager.py
[VIBE_LOGIC]:
- 核心逻辑：测试交互流程的各个环节
- 关键约束：覆盖所有输入验证和错误处理路径
"""

import unittest
from unittest.mock import patch, MagicMock, call
import sys
import io


class TestInteractionManager(unittest.TestCase):
    """交互管理器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.mock_kb = MagicMock()
        self.mock_kb.get_stats.return_value = {'doc_count': 5, 'log_count': 0}
        self.mock_kb.load_index.return_value = True
        self.mock_kb.clear_kb.return_value = None
        self.mock_kb.add_document.return_value = None
        self.mock_kb.ask_stream.return_value = ["测试答案"]
    
    @patch('builtins.input', side_effect=['n'])
    def test_post_demo_exit(self, mock_input):
        """测试演示结束后选择退出"""
        from modules.interaction_manager import InteractionManager
        
        manager = InteractionManager(self.mock_kb)
        
        result = manager.start_post_demo_flow()
        
        self.assertFalse(result)
        mock_input.assert_called_once_with("演示已结束，是否进入交互模式？(y/n): ")
    
    @patch('builtins.input', side_effect=['invalid', 'Y'])
    def test_post_demo_invalid_then_valid(self, mock_input):
        """测试无效输入后输入有效选项"""
        from modules.interaction_manager import InteractionManager
        
        manager = InteractionManager(self.mock_kb)
        manager._handle_index_choice = MagicMock(return_value=True)
        manager._chat_interaction = MagicMock()
        
        result = manager.start_post_demo_flow()
        
        self.assertTrue(result)
        self.assertEqual(mock_input.call_count, 2)
    
    @patch('builtins.input', side_effect=['y', 'a'])
    def test_index_choice_a(self, mock_input):
        """测试选择使用已有索引"""
        from modules.interaction_manager import InteractionManager
        
        manager = InteractionManager(self.mock_kb)
        manager._chat_interaction = MagicMock()
        
        result = manager.start_post_demo_flow()
        
        self.assertTrue(result)
        self.mock_kb.load_index.assert_called_once()
    
    @patch('builtins.input', side_effect=['y', 'b'])
    def test_index_choice_b(self, mock_input):
        """测试选择重新构建索引"""
        from modules.interaction_manager import InteractionManager
        
        manager = InteractionManager(self.mock_kb)
        manager._chat_interaction = MagicMock()
        
        with patch('data.simulated_docs.SIMULATED_DOCS', [
            {'id': 'p1', 'title': 'Test', 'content': 'Test content'}
        ]):
            result = manager.start_post_demo_flow()
        
        self.assertTrue(result)
        self.mock_kb.clear_kb.assert_called_once()
        self.mock_kb.add_document.assert_called_once()
    
    @patch('builtins.input', side_effect=['y', 'invalid', 'A'])
    def test_index_choice_invalid(self, mock_input):
        """测试索引选择时的无效输入"""
        from modules.interaction_manager import InteractionManager
        
        manager = InteractionManager(self.mock_kb)
        manager._chat_interaction = MagicMock()
        
        result = manager.start_post_demo_flow()
        
        self.assertTrue(result)
        self.assertEqual(mock_input.call_count, 3)
    
    def test_validate_input(self):
        """测试输入验证函数"""
        from modules.interaction_manager import InteractionManager
        
        manager = InteractionManager(self.mock_kb)
        
        with patch('builtins.input', side_effect=['invalid', 'y']):
            result = manager._validate_input(
                "prompt: ",
                ['y', 'n'],
                "error"
            )
        
        self.assertEqual(result, 'y')
    
    def test_progress_bar_output(self):
        """测试进度条输出"""
        from modules.interaction_manager import InteractionManager
        
        manager = InteractionManager(self.mock_kb)
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        manager._show_progress_bar(5, 10, prefix="Test:", suffix="(5/10)")
        
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("[=====     ]", output)
        self.assertIn("50.0%", output)


if __name__ == '__main__':
    unittest.main(verbosity=2)