"""
外贸客户开发工作流 - 状态定义
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

# 全局状态
class GlobalState(BaseModel):
    """全局状态定义"""
    # 输入字段
    target_keywords: str = Field(..., description="目标客户关键词，例如：'美国电子产品批发商'")
    website_url: str = Field(default="https://www.aapeakinc.com", description="产品网站URL")
    
    # 中间数据
    product_info: str = Field(default="", description="从网站提取的产品信息")
    customer_list: List[Dict[str, str]] = Field(default=[], description="搜索到的客户列表")
    customers_with_email: List[Dict[str, Any]] = Field(default=[], description="包含邮箱的客户列表")
    email_templates: List[Dict[str, str]] = Field(default=[], description="生成的邮件模板列表")
    
    # 客户洞察和挖掘数据
    customer_insights: Dict[str, Any] = Field(default={}, description="客户洞察分析结果")
    mining_keywords: List[str] = Field(default=[], description="优化后的挖掘关键词")
    mining_strategy: Dict[str, Any] = Field(default={}, description="客户挖掘策略")
    
    # 输出字段
    send_results: Dict[str, Any] = Field(default={}, description="邮件发送结果统计")

# 工作流输入
class GraphInput(BaseModel):
    """工作流的输入"""
    target_keywords: str = Field(..., description="目标客户关键词，例如：'美国电子产品批发商'")
    website_url: str = Field(default="https://www.aapeakinc.com", description="产品网站URL")

# 工作流输出
class GraphOutput(BaseModel):
    """工作流的输出"""
    send_results: Dict[str, Any] = Field(..., description="邮件发送结果统计")

# ========== 节点 1: 产品信息获取节点 ==========
class ProductFetchInput(BaseModel):
    """产品信息获取节点的输入"""
    website_url: str = Field(..., description="产品网站URL")

class ProductFetchOutput(BaseModel):
    """产品信息获取节点的输出"""
    product_info: str = Field(..., description="从网站提取的产品信息")

# ========== 节点 2: 客户搜索节点 ==========
class CustomerSearchInput(BaseModel):
    """客户搜索节点的输入"""
    product_info: str = Field(..., description="产品信息")
    target_keywords: str = Field(..., description="目标客户关键词")

class CustomerSearchOutput(BaseModel):
    """客户搜索节点的输出"""
    customer_list: List[Dict[str, str]] = Field(..., description="搜索到的客户列表")

# ========== 节点 3: 邮箱获取节点 ==========
class EmailFetchInput(BaseModel):
    """邮箱获取节点的输入"""
    customer_list: List[Dict[str, str]] = Field(..., description="客户列表")

class EmailFetchOutput(BaseModel):
    """邮箱获取节点的输出"""
    customers_with_email: List[Dict[str, Any]] = Field(..., description="包含邮箱的客户列表")

# ========== 节点 4: 邮件生成节点 ==========
class EmailGenerateInput(BaseModel):
    """邮件生成节点的输入"""
    product_info: str = Field(..., description="产品信息")
    customers_with_email: List[Dict[str, Any]] = Field(..., description="客户列表")

class EmailGenerateOutput(BaseModel):
    """邮件生成节点的输出"""
    email_templates: List[Dict[str, str]] = Field(..., description="生成的邮件模板列表")

# ========== 节点 5: 邮件发送节点 ==========
class EmailSendInput(BaseModel):
    """邮件发送节点的输入"""
    email_templates: List[Dict[str, str]] = Field(..., description="邮件模板列表")

class EmailSendOutput(BaseModel):
    """邮件发送节点的输出"""
    send_results: Dict[str, Any] = Field(..., description="邮件发送结果统计")

# ========== 节点 6: 客户洞察分析节点 ==========
class CustomerInsightInput(BaseModel):
    """客户洞察分析节点的输入"""
    customer_list: List[Dict[str, str]] = Field(default=[], description="现有客户列表")
    customers_with_email: List[Dict[str, Any]] = Field(default=[], description="包含邮箱的客户列表")
    target_keywords: str = Field(default="", description="目标客户关键词")

class CustomerInsightOutput(BaseModel):
    """客户洞察分析节点的输出"""
    customer_insights: Dict[str, Any] = Field(..., description="客户洞察分析结果，包括地域分布、客户类型、高价值客户等")

# ========== 节点 7: 关键词优化节点 ==========
class KeywordOptimizerInput(BaseModel):
    """关键词优化节点的输入"""
    target_keywords: str = Field(default="", description="原始目标关键词")
    customer_insights: Dict[str, Any] = Field(default={}, description="客户洞察结果")

class KeywordOptimizerOutput(BaseModel):
    """关键词优化节点的输出"""
    mining_keywords: List[str] = Field(..., description="优化后的挖掘关键词列表")
    mining_strategy: Dict[str, Any] = Field(..., description="挖掘策略，包括优先级、地区、客户类型")

# ========== 节点 8: 客户挖掘节点 ==========
class CustomerMiningInput(BaseModel):
    """客户挖掘节点的输入"""
    mining_keywords: List[str] = Field(default=[], description="优化后的挖掘关键词")
    mining_strategy: Dict[str, Any] = Field(default={}, description="挖掘策略")

class CustomerMiningOutput(BaseModel):
    """客户挖掘节点的输出"""
    new_customers: List[Dict[str, str]] = Field(..., description="新挖掘的客户列表")
