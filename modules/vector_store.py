"""
[FILE]: modules/vector_store.py
[ROLE]: 向量存储管理模块，封装 FAISS 索引的创建、保存、加载和操作
[DEPS]: os, shutil, langchain_community (FAISS) | @document_processor.py
[VIBE_LOGIC]:
- 核心逻辑：FAISS 向量数据库的 CRUD 操作，支持 save_local/load_local 持久化
- 关键约束：使用 FAISS CPU 版本，加载时设置 allow_dangerous_deserialization=True
"""

import os
import shutil
from langchain_community.vectorstores import FAISS


class VectorStoreManager:
    """
    FAISS 向量存储管理器
    
    负责 FAISS 索引的创建、保存、加载和操作，使用 CPU 版本。
    """
    
    def __init__(self, persist_dir, embeddings):
        """
        初始化向量存储管理器
        
        Args:
            persist_dir: 索引持久化目录路径
            embeddings: 向量化模型实例（OpenAIEmbeddings）
        """
        self.persist_dir = persist_dir
        self.embeddings = embeddings
        self.vector_store = None
    
    def create_index(self, documents):
        """
        从文档列表创建 FAISS 索引
        
        Args:
            documents: Document 对象列表
        """
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
    
    def save_index(self):
        """
        将索引保存到本地持久化目录
        """
        if self.vector_store:
            os.makedirs(self.persist_dir, exist_ok=True)
            self.vector_store.save_local(self.persist_dir)
    
    def load_index(self):
        """
        从本地加载 FAISS 索引
        
        Returns:
            bool: 加载成功返回 True，失败返回 False
        """
        if os.path.exists(self.persist_dir) and os.listdir(self.persist_dir):
            self.vector_store = FAISS.load_local(
                self.persist_dir,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            return True
        return False
    
    def add_documents(self, documents):
        """
        向现有索引添加文档
        
        Args:
            documents: Document 对象列表
        """
        if self.vector_store:
            self.vector_store.add_documents(documents)
    
    def delete_documents_by_id(self, doc_id):
        """
        根据文档 ID 删除文档
        
        Args:
            doc_id: 要删除的文档 ID
        
        Note:
            FAISS 不支持直接删除，通过重建索引实现
        """
        if self.vector_store:
            all_docs = self.vector_store.get_documents()
            remaining_docs = [
                doc for doc in all_docs 
                if doc.metadata.get("doc_id") != doc_id
            ]
            
            if remaining_docs:
                self.vector_store = FAISS.from_documents(remaining_docs, self.embeddings)
            else:
                self.vector_store = None
    
    def clear_index(self):
        """
        清空整个索引
        """
        self.vector_store = None
        if os.path.exists(self.persist_dir):
            shutil.rmtree(self.persist_dir)
            os.makedirs(self.persist_dir)
    
    def similarity_search(self, query, k=5):
        """
        执行相似度搜索
        
        Args:
            query: 查询字符串
            k: 返回结果数量（默认 5）
        
        Returns:
            list: (Document, similarity_score) 元组列表，按相似度降序排列
        """
        if self.vector_store:
            return self.vector_store.similarity_search_with_score(query, k=k)
        return []
    
    def search(self, query, k=5):
        """
        执行相似度搜索（简化接口）
        
        Args:
            query: 查询字符串
            k: 返回结果数量（默认 5）
        
        Returns:
            list: Document 对象列表，按相似度降序排列
        """
        if self.vector_store:
            return self.vector_store.similarity_search(query, k=k)
        return []
    
    def backup_index(self, backup_dir):
        """
        备份索引到指定目录
        
        Args:
            backup_dir: 备份目录路径
        """
        if os.path.exists(self.persist_dir):
            if os.path.exists(backup_dir):
                shutil.rmtree(backup_dir)
            shutil.copytree(self.persist_dir, backup_dir)
    
    def get_doc_count(self):
        """
        获取索引中的文档数量，使用安全、高效、兼容多向量库地获取索引文档数量
        
        Returns:
            int: 文档数量
        """
        if self.vector_store:
            if hasattr(self.vector_store, 'index') and hasattr(self.vector_store.index, 'ntotal'):
                return self.vector_store.index.ntotal
            elif hasattr(self.vector_store, '_index_to_docstore_id'):
                return len(self.vector_store._index_to_docstore_id)
            else:
                return 0
        return 0