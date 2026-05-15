"""
[FILE]: core/__init__.py
[ROLE]: 核心模块导出文件
[DEPS]: None | @core/model_factory.py
[VIBE_LOGIC]:
- 核心逻辑：导出模型工厂的核心接口
- 关键约束：统一对外提供 get_llm, get_embeddings, get_model_info 函数
"""

from .model_factory import get_llm, get_embeddings, get_model_info

__all__ = ['get_llm', 'get_embeddings', 'get_model_info']