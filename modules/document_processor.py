"""
[FILE]: modules/document_processor.py
[ROLE]: 文档处理模块，负责文档加载、文本分块和元数据管理
[DEPS]: langchain_text_splitters (RecursiveCharacterTextSplitter), langchain_core (Document) | None
[VIBE_LOGIC]:
- 核心逻辑：使用 RecursiveCharacterTextSplitter 进行文本分块，支持单文档和多文档分块
- 关键约束：分块大小 500 字符，重叠 50 字符，分隔符优先中文标点（句号、分号、换行）
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class DocumentProcessor:
    """
    文档处理类，负责文档加载、文本分块和元数据管理
    
    关键参数：
        chunk_size: 分块大小，默认 500 字符
        chunk_overlap: 块之间的重叠字符数，默认 50 字符
        separators: 分隔符列表，优先使用中文标点
    """
    
    def __init__(self, chunk_size=500, chunk_overlap=50):
        """
        初始化文档处理器
        
        Args:
            chunk_size: 每个块的最大字符数（默认 500）
            chunk_overlap: 块之间的重叠字符数（默认 50）
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",      # 双换行
                "\n",        # 换行
                "。",         # 中文句号
                "；",         # 中文分号
                "；",         # 中文分号（全角）
                "，",         # 中文逗号
                " ",          # 空格
                ".",          # 英文句号
                ";",          # 英文分号
                ",",          # 英文逗号
            ],
            length_function=len,
        )
    
    def split_document(self, doc_id, title, content):
        """
        将单个文档分块
        
        Args:
            doc_id: 文档唯一标识
            title: 文档标题
            content: 文档内容
            
        Returns:
            list[Document]: 分块后的 Document 对象列表，每个对象包含元数据
        """
        chunks = self.text_splitter.split_text(content)
        documents = []
        
        for chunk_index, chunk_content in enumerate(chunks):
            metadata = {
                "doc_id": doc_id,
                "title": title,
                "chunk_index": chunk_index,
                "total_chunks": len(chunks),
            }
            doc = Document(page_content=chunk_content, metadata=metadata)
            documents.append(doc)
        
        return documents
    
    def split_documents(self, docs_list):
        """
        将文档列表批量分块
        
        Args:
            docs_list: 文档字典列表，每个字典包含 id、title、content
            
        Returns:
            list[Document]: 所有文档分块后的 Document 对象列表
        """
        all_chunks = []
        
        for doc in docs_list:
            doc_id = doc.get("id", "")
            title = doc.get("title", "")
            content = doc.get("content", "")
            
            if not doc_id or not title or not content:
                continue
            
            chunks = self.split_document(doc_id, title, content)
            all_chunks.extend(chunks)
        
        return all_chunks
    
    def get_chunk_info(self, doc):
        """
        获取文档块的元信息
        
        Args:
            doc: Document 对象
            
        Returns:
            dict: 包含文档 ID、标题、块索引、总块数的字典
        """
        return {
            "doc_id": doc.metadata.get("doc_id", "unknown"),
            "title": doc.metadata.get("title", "unknown"),
            "chunk_index": doc.metadata.get("chunk_index", 0),
            "total_chunks": doc.metadata.get("total_chunks", 1),
            "content_length": len(doc.page_content),
        }