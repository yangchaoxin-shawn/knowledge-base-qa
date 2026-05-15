"""
[FILE]: core/model_factory.py
[ROLE]: 模型工厂模块，提供统一的模型初始化功能
[DEPS]: os, dotenv, langchain_openai (ChatOpenAI, OpenAIEmbeddings) | None
[VIBE_LOGIC]:
- 核心逻辑：封装 LLM 和向量化模型的初始化，从 .env 文件读取配置
- 关键约束：LangChain 1.0+, 使用硅基流动 API, 默认模型 Qwen/Qwen3-8B 和 BAAI/bge-m3
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def get_llm(model_name="Qwen/Qwen3-8B", **kwargs):
    """
    获取 ChatOpenAI 模型实例
    
    Args:
        model_name: 模型名称（默认：Qwen/Qwen3-8B）
        **kwargs: 其他模型参数（temperature, max_tokens, timeout 等）
    
    Returns:
        ChatOpenAI 模型实例
    """
    load_dotenv()
    
    api_key = os.getenv("SILICONFLOW_API_KEY") 
    api_base = os.getenv("SILICONFLOW_API_BASE", "https://api.siliconflow.cn/v1")
    
    if not api_key:
        raise ValueError("请配置 SILICONFLOW_API_KEY 环境变量")
    
    defaults = {
        "temperature": 0.7,
        "max_tokens": 2048,
        "timeout": 30,
        "max_retries": 1,
        "streaming": kwargs.get("streaming", False)
    }
    
    params = {**defaults, **kwargs}
    
    llm = ChatOpenAI(
        api_key=api_key,
        base_url=api_base,
        model=model_name,
        **params
    )
    
    return llm


def get_embeddings(model_name="BAAI/bge-m3", **kwargs):
    """
    获取 OpenAI 兼容的向量化模型实例
    
    Args:
        model_name: 向量化模型名称（默认：BAAI/bge-m3）
        **kwargs: 其他模型参数
    
    Returns:
        OpenAIEmbeddings 实例
    """
    load_dotenv()
    
    api_key = os.getenv("SILICONFLOW_API_KEY")
    api_base = os.getenv("SILICONFLOW_API_BASE", "https://api.siliconflow.cn/v1")
    
    if not api_key:
        raise ValueError("请配置 SILICONFLOW_API_KEY 环境变量")
    
    default_params = {
        "model": model_name,
        "api_key": api_key,
        "base_url": api_base,
    }
    
    params = {**default_params, **kwargs}
    return OpenAIEmbeddings(**params)


def get_model_info(llm):
    """
    获取模型信息
    
    Returns:
        包含模型信息的字典
    """
    load_dotenv()
    api_base = os.getenv("SILICONFLOW_API_BASE") or "https://api.siliconflow.cn/v1"
    
    return {
        "model": llm.model_name,
        "api_base": api_base,
        "temperature": getattr(llm, "temperature", "未知"),
        "max_tokens": getattr(llm, "max_tokens", "未知"),
        "streaming": getattr(llm, "streaming", False)
    }


if __name__ == "__main__":
    print("Model Factory Test")
    print("=" * 40)
    
    try:
        llm = get_llm()
        info = get_model_info(llm)
        print(f"Model: {info['model']}")
        print(f"API Base: {info['api_base']}")
        print("Test passed!")
    except Exception as e:
        print(f"Error: {e}")