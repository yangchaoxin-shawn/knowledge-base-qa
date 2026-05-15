"""
[FILE]: modules/qa_engine.py
[ROLE]: 问答引擎模块，实现 RAG 问答流程
[DEPS]: langchain_core (StrOutputParser, RunnablePassthrough) | @retriever.py, @prompts.py
[VIBE_LOGIC]:
- 核心逻辑：拼接检索文档为上下文，构建 LCEL 链调用 LLM 生成答案，提取溯源信息
- 关键约束：使用 ChatOpenAI，model=Qwen/Qwen3-8B，temperature=0.1，max_tokens=1024
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from config.prompts import RAG_PROMPT_TEMPLATE, format_context, get_sources


class QAEngine:
    """
    RAG 问答引擎
    
    负责将检索到的文档拼接为上下文，构建 LCEL 链调用 LLM 生成答案，并提取溯源信息。
    """
    
    def __init__(self, llm, retriever):
        """
        初始化问答引擎
        
        Args:
            llm: ChatOpenAI 模型实例
            retriever: Retriever 实例
        """
        self.llm = llm
        self.retriever = retriever
        self._build_chain()
    
    def _build_chain(self):
        """构建 LCEL RAG 链"""
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=RAG_PROMPT_TEMPLATE
        )
        
        self.rag_chain = (
            {
                "context": lambda x: format_context(self.retriever.retrieve(x["question"])),
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    def ask(self, question, k=5):
        """
        执行 RAG 问答
        
        Args:
            question: 用户问题
            k: 检索文档数量（默认 5）
        
        Returns:
            tuple: (answer, sources) - 答案和来源列表
        """
        docs = self.retriever.retrieve(question, k=k)
        
        if not docs:
            return "根据现有知识无法回答", []
        
        context = format_context(docs)
        prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)
        
        response = self.llm.invoke(prompt)
        answer = response.content
        
        sources = get_sources(docs)
        
        return answer, sources
    
    def ask_with_lcel(self, question):
        """
        使用 LCEL 链执行问答
        
        Args:
            question: 用户问题
        
        Returns:
            str: 答案
        """
        return self.rag_chain.invoke({"question": question})
    
    def stream_ask(self, question, k=5):
        """
        流式问答（逐步返回答案）
        
        Args:
            question: 用户问题
            k: 检索文档数量（默认 5）
        
        Yields:
            str: 答案片段
        """
        docs = self.retriever.retrieve(question, k=k)
        
        if not docs:
            yield "根据现有知识无法回答"
            return
        
        context = format_context(docs)
        prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)
        
        for chunk in self.llm.stream(prompt):
            yield chunk.content
    
    def _get_sources(self, docs):
        """
        从文档列表中提取来源标题
        
        Args:
            docs: Document 对象列表
        
        Returns:
            list: 来源标题列表
        """
        return get_sources(docs)