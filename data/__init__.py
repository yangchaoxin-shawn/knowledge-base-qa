"""
[FILE]: data/__init__.py
[ROLE]: 数据模块初始化文件，导出模拟文档数据
[DEPS]: Python Standard Library | @simulated_docs.py
[VIBE_LOGIC]:
- 核心逻辑：声明 data 模块的公共接口，导出 SIMULATED_DOCS
- 关键约束：无
"""

from .simulated_docs import SIMULATED_DOCS, get_doc_by_id, get_all_docs, get_doc_titles

__all__ = ["SIMULATED_DOCS", "get_doc_by_id", "get_all_docs", "get_doc_titles"]