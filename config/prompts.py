"""
[FILE]: config/prompts.py
[ROLE]: RAG 提示词模板管理，定义问答系统的提示词格式
[DEPS]: None | None
[VIBE_LOGIC]:
- 核心逻辑：定义包含角色、上下文、问题和溯源要求的提示词模板
- 关键约束：答案必须基于上下文，未知时返回"根据现有知识无法回答"，末尾注明来源格式（来源：文档标题）
"""

RAG_PROMPT_TEMPLATE = """你是一个企业知识库助手，请基于以下上下文回答问题。

上下文：
{context}

问题：{question}

请按照以下要求回答：
1. 答案必须基于提供的上下文内容
2. 如果不知道答案，就说"根据现有知识无法回答"
3. 在答案末尾用括号注明信息来源，格式如（来源：文档标题1、文档标题2）

答案："""

RAG_PROMPT_TEMPLATE_SHORT = """基于以下上下文回答问题：

{context}

问题：{question}

答案（需注明来源）："""

SUMMARIZE_PROMPT = """请对以下文档内容进行总结：

{context}

总结："""

QUESTION_REWRITE_PROMPT = """请将以下问题改写为更清晰的表达方式：

原问题：{question}

改写后的问题："""

def format_context(docs):
    """
    将文档列表格式化为上下文字符串
    
    Args:
        docs: Document 对象列表
        
    Returns:
        str: 格式化后的上下文字符串
    """
    context_parts = []
    for doc in docs:
        title = doc.metadata.get("title", "Unknown")
        content = doc.page_content
        context_parts.append(f"【{title}】\n{content}")
    return "\n\n".join(context_parts)

def get_sources(docs):
    """
    从文档列表中提取来源标题
    
    Args:
        docs: Document 对象列表
        
    Returns:
        list: 来源标题列表（去重）
    """
    return list(set(doc.metadata.get("title", "Unknown") for doc in docs))