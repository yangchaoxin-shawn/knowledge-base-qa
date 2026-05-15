"""
[FILE]: config/settings.py
[ROLE]: 系统配置管理，集中存储 API 密钥、路径、模型参数等配置项，从 .env 文件读取环境变量
[DEPS]: os, dotenv | None
[VIBE_LOGIC]:
- 核心逻辑：使用 dotenv 加载项目内的 .env 文件，定义 API 配置、模型参数、演示问题列表、目录路径
- 关键约束：LangChain 1.0, SILICONFLOW_API_BASE=https://api.siliconflow.cn/v1, EMBEDDING_MODEL=BAAI/bge-m3, LLM_MODEL=Qwen/Qwen3-8B, DEFAULT_K=5, 使用 FAISS CPU 版本
"""

import os
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)

load_dotenv(os.path.join(project_dir, ".env"))

# API configurations
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
SILICONFLOW_API_BASE = os.getenv("SILICONFLOW_API_BASE", "https://api.siliconflow.cn/v1")

# Model configurations
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
LLM_MODEL = os.getenv("LLM_MODEL", "Qwen/Qwen3-8B")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))

# FAISS configuration
FAISS_PERSIST_DIRECTORY = os.path.join(project_dir, "data", "faiss_index")

# Log configuration
LOGS_DIRECTORY = os.path.join(project_dir, "logs")

# Retrieval configuration
DEFAULT_K = int(os.getenv("DEFAULT_K", "5"))

# Demo questions
DEMO_QUESTIONS = [
    "你们公司有哪些产品？",
    "智能客服机器人的收费标准是什么？",
    "数据分析平台支持哪些数据源？",
    "企业知识库系统有什么功能？",
    "如何购买企业版？"
]

# Ensure directories exist
os.makedirs(FAISS_PERSIST_DIRECTORY, exist_ok=True)
os.makedirs(LOGS_DIRECTORY, exist_ok=True)

# Validation
if not SILICONFLOW_API_KEY:
    print("警告：SILICONFLOW_API_KEY 环境变量未设置，请在 .env 文件中配置")