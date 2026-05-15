"""
[FILE]: kb_manager.py
[ROLE]: KnowledgeBaseManager 核心类，封装知识库的完整生命周期管理
[DEPS]: os | @core/model_factory.py, @modules/document_processor.py, @modules/vector_store.py, @modules/retriever.py, @modules/qa_engine.py, @modules/log_manager.py, @data/simulated_docs.py
[VIBE_LOGIC]:
- 核心逻辑：整合文档处理、向量存储、检索、问答、日志模块，提供统一的知识库操作接口
- 关键约束：LangChain 1.0, 使用 get_llm(Qwen/Qwen3-8B) 和 get_embeddings(BAAI/bge-m3)
"""

import os
from core.model_factory import get_llm, get_embeddings
from modules.document_processor import DocumentProcessor
from modules.vector_store import VectorStoreManager
from modules.retriever import Retriever
from modules.qa_engine import QAEngine
from modules.log_manager import LogManager
from data.simulated_docs import SIMULATED_DOCS


class KnowledgeBaseManager:
    """
    知识库管理器
    
    封装知识库的完整生命周期管理，包括索引创建、加载、文档管理、问答等功能。
    """
    
    def __init__(self, persist_dir="./data/faiss_index", load_existing=False):
        """
        初始化知识库管理器
        
        Args:
            persist_dir: FAISS 索引持久化目录
            load_existing: 是否加载现有索引
        """
        self.persist_dir = persist_dir
        
        self.embeddings = get_embeddings(model_name="BAAI/bge-m3")
        self.llm = get_llm(model_name="Qwen/Qwen3-8B", temperature=0.1, max_tokens=1024)
        
        self.document_processor = DocumentProcessor()
        self.vector_store_manager = VectorStoreManager(persist_dir, self.embeddings)
        self.retriever = Retriever(self.vector_store_manager)
        self.qa_engine = QAEngine(self.llm, self.retriever)
        self.log_manager = LogManager(log_dir="./logs")
        
        if load_existing:
            success = self.vector_store_manager.load_index()
            if not success:
                print("加载失败，重新构建索引...")
                self.build_from_docs(SIMULATED_DOCS)
        else:
            self.build_from_docs(SIMULATED_DOCS)
    
    def build_from_docs(self, docs_list):
        """
        从文档列表构建索引
        
        Args:
            docs_list: 文档字典列表
        """
        chunks = self.document_processor.split_documents(docs_list)
        self.vector_store_manager.create_index(chunks)
        self.vector_store_manager.save_index()
    
    def save_index(self):
        """保存索引到本地"""
        self.vector_store_manager.save_index()
    
    def load_index(self):
        """加载本地索引"""
        return self.vector_store_manager.load_index()
    
    def add_document(self, title, content, doc_id=None):
        """
        添加新文档到知识库
        
        Args:
            title: 文档标题
            content: 文档内容
            doc_id: 文档 ID（可选，自动生成）
        """
        if doc_id is None:
            doc_id = f"doc_{hash(title)}_{self.vector_store_manager.get_doc_count() + 1}"
        
        chunks = self.document_processor.split_document(doc_id, title, content)
        self.vector_store_manager.add_documents(chunks)
        self.vector_store_manager.save_index()
    
    def delete_document(self, doc_id):
        """
        根据文档 ID 删除文档
        
        Args:
            doc_id: 文档 ID
        """
        self.vector_store_manager.delete_documents_by_id(doc_id)
        self.vector_store_manager.save_index()
    
    def clear_kb(self):
        """清空知识库"""
        self.vector_store_manager.clear_index()
    
    def retrieve(self, query, k=5):
        """
        检索相似文档
        
        Args:
            query: 查询字符串
            k: 返回数量（默认 5）
        
        Returns:
            list: Document 对象列表
        """
        return self.retriever.retrieve(query, k=k)
    
    def ask(self, question, k=5):
        """
        执行 RAG 问答
        
        Args:
            question: 用户问题
            k: 检索数量（默认 5）
        
        Returns:
            tuple: (answer, sources) - 答案和来源列表
        """
        answer, sources = self.qa_engine.ask(question, k=k)
        
        docs = self.retriever.retrieve(question, k=k)
        self.log_manager.log_query(question, docs, answer)
        
        return answer, sources
    
    def ask_stream(self, question, k=5):
        """
        流式执行 RAG 问答
        
        Args:
            question: 用户问题
            k: 检索数量（默认 5）
        
        Yields:
            答案片段（字符串）或来源列表
        """
        for chunk in self.qa_engine.stream_ask(question, k=k):
            yield chunk
        
        docs = self.retriever.retrieve(question, k=k)
        sources = list(set([doc.metadata.get('title', '未知') for doc in docs]))
        yield sources
        
        self.log_manager.log_query(question, docs, "streaming answer")
    
    def log_query(self, question, docs, answer):
        """
        记录查询日志
        
        Args:
            question: 用户问题
            docs: 检索到的文档列表
            answer: 答案
        """
        self.log_manager.log_query(question, docs, answer)
    
    def export_logs(self, file_path):
        """
        导出日志
        
        Args:
            file_path: 输出文件路径
        """
        self.log_manager.export_logs(file_path)
    
    def get_stats(self):
        """
        获取知识库统计信息
        
        Returns:
            dict: 统计信息
        """
        return {
            "doc_count": self.vector_store_manager.get_doc_count(),
            "log_count": self.log_manager.get_log_count()
        }