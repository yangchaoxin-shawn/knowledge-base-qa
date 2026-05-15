# 企业知识库问答系统

基于 LangChain 1.0 + FAISS + 硅基流动平台 API 构建的轻量级 RAG（Retrieval-Augmented Generation）问答系统。

## 功能特性

- ✅ **模拟数据**：产品介绍、收费方案等信息直接存储在 Python 变量中
- ✅ **向量化模型**：硅基流动 `BAAI/bge-m3`（通过 OpenAI 兼容接口调用）
- ✅ **LLM**：硅基流动 `Qwen/Qwen3-8B`（ChatOpenAI 方式）
- ✅ **向量数据库**：FAISS（CPU 版本，本地持久化）
- ✅ **检索排序**：直接使用 FAISS 的余弦相似度得分，不引入额外重排序器
- ✅ **答案溯源**：在生成答案时标注引用文档来源
- ✅ **管理功能**：文档增删、数据库备份/清空、查询日志记录
- ✅ **启动流程**：索引选择 → 演示问答 → 可选交互模式
- ✅ **流式输出**：答案以流式方式逐步显示，提高阅读体验

## 项目结构

```
knowledge_base_qa/
├── config/                  # 配置文件
│   ├── __init__.py
│   ├── settings.py          # 系统配置（API密钥、路径、模型参数）
│   └── prompts.py           # 提示词模板
├── data/                    # 数据目录
│   ├── __init__.py
│   ├── simulated_docs.py    # 模拟文档数据
│   └── faiss_index/         # FAISS 索引持久化目录
├── modules/                 # 功能模块
│   ├── __init__.py
│   ├── document_processor.py # 文档处理（分块）
│   ├── vector_store.py      # 向量存储管理（FAISS）
│   ├── retriever.py         # 文档检索
│   ├── qa_engine.py         # RAG 问答引擎
│   ├── log_manager.py       # SQLite 日志管理
│   └── interaction_manager.py # 用户交互流程管理
├── utils/                   # 工具函数
│   ├── __init__.py
│   └── helpers.py           # 辅助函数
├── logs/                    # SQLite 日志文件目录
├── kb_manager.py            # KnowledgeBaseManager 核心类
├── main.py                  # 主程序入口
├── run_demo.py              # 演示模式脚本
├── test_interaction.py      # 交互流程测试
├── requirements.txt         # 依赖清单
└── README.md                # 项目说明文档
```

## 快速开始

### 环境要求

- Python 3.10+
- 硅基流动平台 API Key（注册地址：https://www.siliconflow.cn/）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

在项目根目录（`ai_application_development_learning/`）下的 `.env` 文件中配置：

```ini
# 硅基流动 API 配置
SILICONFLOW_API_KEY=your_api_key_here
SILICONFLOW_API_BASE=https://api.siliconflow.cn/v1

# 模型配置
EMBEDDING_MODEL=BAAI/bge-m3
LLM_MODEL=Qwen/Qwen3-8B
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1024

# 检索配置
DEFAULT_K=5
```

### 运行方式

#### 演示模式（自动运行内置问题）

```bash
python run_demo.py
```

#### 主程序（包含完整交互流程）

```bash
python main.py
```

### 交互流程

1. **演示阶段**：系统自动运行 5 个内置问题的问答演示
2. **模式选择**：演示结束后询问是否进入交互模式（y/n）
3. **索引管理**：
   - `a)` 使用已有的索引
   - `b)` 重新构建索引（全量重构）
4. **交互问答**：输入问题进行问答，输入 `q` 或 `exit` 退出

## 核心模块说明

### KnowledgeBaseManager

知识库管理器，封装知识库的完整生命周期管理：

| 方法 | 功能 |
|------|------|
| `__init__(persist_dir, load_existing)` | 初始化，根据参数决定加载或重建索引 |
| `build_from_docs(docs_list)` | 从文档列表构建索引 |
| `save_index()` | 持久化 FAISS 索引到本地 |
| `load_index()` | 从本地加载 FAISS 索引 |
| `add_document(title, content, doc_id)` | 添加新文档 |
| `delete_document(doc_id)` | 根据 doc_id 删除文档 |
| `clear_kb()` | 清空知识库 |
| `retrieve(query, k=5)` | 返回相似度排序后的文档块列表 |
| `ask(question, k=5)` | 执行 RAG 问答，返回答案和溯源信息 |
| `ask_stream(question, k=5)` | 流式执行 RAG 问答 |
| `log_query(question, docs, answer)` | 记录查询日志 |
| `export_logs(file_path)` | 导出日志 |

### QAEngine

问答引擎，实现 RAG 问答流程：

- 使用 LCEL（LangChain Expression Language）构建问答链
- 支持同步调用和流式输出
- 自动提取和标注答案来源

### DocumentProcessor

文档处理器，负责文本分块：

- 使用 `RecursiveCharacterTextSplitter`
- 分块大小：500 字符
- 重叠大小：50 字符
- 优先使用中文标点分隔

## 技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| LangChain | 1.0+ | 大语言模型应用框架 |
| FAISS | CPU | 向量数据库 |
| OpenAIEmbeddings | - | 向量化模型封装 |
| ChatOpenAI | - | LLM 模型封装 |
| SQLite | - | 日志存储 |

## 输出示例

```
问题：你们公司有哪些产品？

答案：根据提供的上下文，公司有以下产品：
1. 数据分析平台（支持数据可视化、分析及预警功能）
2. 智能客服机器人（基于大语言模型的对话系统）
3. 企业知识库系统（知识资产管理与共享平台）
（来源：数据分析平台、智能客服机器人、企业知识库系统）
--------------------------------------------------
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！