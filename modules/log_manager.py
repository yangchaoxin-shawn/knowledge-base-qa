"""
[FILE]: modules/log_manager.py
[ROLE]: 日志管理模块，使用 SQLite 记录查询日志
[DEPS]: os, sqlite3, json, datetime | None
[VIBE_LOGIC]:
- 核心逻辑：创建 query_logs 表，记录 timestamp、question、retrieved_chunks、answer、feedback
- 关键约束：retrieved_chunks 存储 JSON 格式，feedback 为整数类型（0/1/None）
"""

import os
import sqlite3
import json
from datetime import datetime


class LogManager:
    """
    查询日志管理器
    
    使用 SQLite 数据库记录查询日志，包括时间戳、问题、检索到的文档块、答案和反馈。
    """
    
    def __init__(self, log_dir):
        """
        初始化日志管理器
        
        Args:
            log_dir: 日志目录路径
        """
        self.db_path = os.path.join(log_dir, "query_logs.db")
        self._init_db()
    
    def _init_db(self):
        """初始化 SQLite 数据库和表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                question TEXT NOT NULL,
                retrieved_chunks TEXT,
                answer TEXT NOT NULL,
                feedback INTEGER DEFAULT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def log_query(self, question, docs, answer):
        """
        记录查询日志
        
        Args:
            question: 用户问题
            docs: 检索到的 Document 对象列表
            answer: 生成的答案
        """
        timestamp = datetime.now().isoformat()
        
        chunks_info = []
        for doc in docs:
            chunks_info.append({
                "title": doc.metadata.get("title", "Unknown"),
                "content_preview": doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content,
                "doc_id": doc.metadata.get("doc_id", "Unknown")
            })
        
        retrieved_chunks_json = json.dumps(chunks_info, ensure_ascii=False)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO query_logs (timestamp, question, retrieved_chunks, answer)
            VALUES (?, ?, ?, ?)
        """, (timestamp, question, retrieved_chunks_json, answer))
        
        conn.commit()
        conn.close()
    
    def get_logs(self, limit=100):
        """
        获取最近的日志记录
        
        Args:
            limit: 最大返回数量（默认 100）
        
        Returns:
            list: 日志记录列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM query_logs ORDER BY id DESC LIMIT ?
        """, (limit,))
        
        logs = cursor.fetchall()
        conn.close()
        
        return logs
    
    def export_logs(self, file_path):
        """
        导出日志到 JSON 文件
        
        Args:
            file_path: 输出文件路径
        """
        logs = self.get_logs(limit=10000)
        
        formatted_logs = []
        for log in logs:
            formatted_logs.append({
                "id": log[0],
                "timestamp": log[1],
                "question": log[2],
                "retrieved_chunks": json.loads(log[3]) if log[3] else [],
                "answer": log[4],
                "feedback": log[5]
            })
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(formatted_logs, f, ensure_ascii=False, indent=2)
    
    def add_feedback(self, log_id, feedback):
        """
        添加反馈到日志记录
        
        Args:
            log_id: 日志记录 ID
            feedback: 反馈值（0 或 1）
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE query_logs SET feedback = ? WHERE id = ?
        """, (feedback, log_id))
        
        conn.commit()
        conn.close()
    
    def get_log_count(self):
        """
        获取日志记录总数
        
        Returns:
            int: 日志记录数量
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM query_logs")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count