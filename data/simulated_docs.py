"""
[FILE]: data/simulated_docs.py
[ROLE]: 模拟文档数据源，存储产品介绍、收费方案等知识库内容
[DEPS]: Python Standard Library | None
[VIBE_LOGIC]:
- 核心逻辑：使用 Python 字典列表存储文档，每个元素包含 id、title、content
- 关键约束：文档格式必须包含 id、title、content 三个字段
"""

SIMULATED_DOCS = [
    {
        "id": "p1",
        "title": "智能客服机器人",
        "content": "智能客服机器人是一款基于大语言模型的智能对话系统，支持多轮对话、意图识别、实体提取等功能。产品特点包括7x24小时不间断服务、多渠道接入能力、智能路由分配以及数据分析报表功能。收费方案分为三个档次：基础版每年9999元，专业版每年29999元，企业版需要定制报价。"
    },
    {
        "id": "p2",
        "title": "数据分析平台",
        "content": "数据分析平台提供企业级数据可视化和分析能力。支持的数据源包括MySQL、PostgreSQL、MongoDB、Oracle、SQL Server、CSV文件以及Excel文件。核心功能包括数据清洗、可视化图表展示、智能分析报告生成以及数据预警机制。"
    },
    {
        "id": "p3",
        "title": "企业知识库系统",
        "content": "企业知识库系统帮助企业管理和共享知识资产。核心功能包括文档管理、智能检索、版本控制、权限管理和知识图谱。支持多种文档格式：PDF、Word、Markdown和图片。系统支持与OA、CRM等系统集成，实现知识共享和业务流程的无缝衔接。"
    },
    {
        "id": "p4",
        "title": "收费方案",
        "content": "所有产品均提供免费试用版，试用期为14天。购买方式支持年付和月付，年付享受8折优惠。企业版支持定制开发，价格根据具体需求面议。支付方式包括在线支付、银行转账，并支持发票开具。"
    },
    {
        "id": "p5",
        "title": "产品更新日志",
        "content": "2025年Q1更新包括新增多语言支持、优化检索算法以及增加API接口。2024年Q2计划推出移动端APP、增强数据分析功能以及优化用户界面设计。"
    }
]


def get_doc_by_id(doc_id):
    """
    根据文档ID获取文档
    
    Args:
        doc_id: 文档ID
        
    Returns:
        文档字典，如果未找到返回None
    """
    for doc in SIMULATED_DOCS:
        if doc["id"] == doc_id:
            return doc
    return None


def get_all_docs():
    """
    获取所有文档
    
    Returns:
        文档列表的副本
    """
    return [doc.copy() for doc in SIMULATED_DOCS]


def get_doc_titles():
    """
    获取所有文档标题
    
    Returns:
        标题列表
    """
    return [doc["title"] for doc in SIMULATED_DOCS]