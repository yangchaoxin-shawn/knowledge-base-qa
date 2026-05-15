"""
[FILE]: modules/retriever.py
[ROLE]: 文档检索模块，执行相似度搜索并返回排序后的文档块
[DEPS]: None | @vector_store.py
[VIBE_LOGIC]:
- 核心逻辑：调用 FAISS similarity_search，按余弦相似度排序返回 Top-K 结果
- 关键约束：不引入额外重排序器，直接使用 FAISS 返回顺序，默认 k=5
"""

from .vector_store import VectorStoreManager


class Retriever:
    """
    文档检索器
    
    负责执行相似度搜索，直接使用 FAISS 的余弦相似度排序结果，不引入额外重排序器。
    """
    
    def __init__(self, vector_store_manager: VectorStoreManager):
        """
        初始化检索器
        
        Args:
            vector_store_manager: VectorStoreManager 实例
        """
        self.vector_store_manager = vector_store_manager
    
    def retrieve(self, query, k=5):
        """
        检索与查询最相似的文档块
        
        Args:
            query: 查询字符串
            k: 返回的文档数量（默认 5）
        
        Returns:
            list: Document 对象列表，按余弦相似度从高到低排序
        """
        results = self.vector_store_manager.similarity_search(query, k=k)
        results.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, score in results]
    
    def retrieve_with_scores(self, query, k=5):
        """
        检索与查询最相似的文档块（带相似度分数）
        
        Args:
            query: 查询字符串
            k: 返回的文档数量（默认 5）
        
        Returns:
            list: (Document, similarity_score) 元组列表，按相似度降序排列
        """
        results = self.vector_store_manager.similarity_search(query, k=k)
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def get_top_k(self, query, k=5):
        """
        获取 Top-K 相似文档（简化接口）
        
        Args:
            query: 查询字符串
            k: 返回的文档数量（默认 5）
        
        Returns:
            list: Document 对象列表，按余弦相似度从高到低排序
        """
        return self.retrieve(query, k=k)
    
    def get_sources(self, query, k=5):
        """
        获取检索结果的来源文档标题列表
        
        Args:
            query: 查询字符串
            k: 返回的文档数量（默认 5）
        
        Returns:
            list: 来源文档标题列表（去重）
        """
        docs = self.retrieve(query, k=k)
        sources = list(set(doc.metadata.get("title", "Unknown") for doc in docs))
        return sources