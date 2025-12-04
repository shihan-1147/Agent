"""Agent核心逻辑 - ReAct循环"""
import json
from openai import OpenAI
from tools import get_weather, search_nearby, search_knowledge_base


# 工具描述 Schema
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "查询关于小米YU7汽车的详细信息、配置、参数、手册内容等。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "需要查询的具体问题，例如：YU7的续航是多少"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_nearby",
            "description": "搜索指定城市的附近商家、地点（如小米之家）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "搜索关键词"},
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["keyword", "city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市当天的天气情况。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
            }
        }
    }
]


class AgentCore:
    """Agent核心类 - 负责ReAct循环逻辑"""
    
    def __init__(self, api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"):
        """
        初始化Agent
        
        Args:
            api_key: API密钥
            base_url: API基础URL
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.tools_schema = TOOLS_SCHEMA
        self.tool_functions = {
            "search_knowledge_base": search_knowledge_base,
            "search_nearby": search_nearby,
            "get_weather": get_weather
        }
    
    def run_agent(self, messages, model="qwen-plus", callback=None):
        """
        运行Agent的ReAct循环
        
        Args:
            messages: 对话历史消息列表
            model: 使用的模型名称
            callback: 回调函数，用于UI更新 callback(event_type, data)
                event_type: 'thinking' | 'tool_call' | 'tool_result' | 'response' | 'error'
        
        Returns:
            tuple: (最终回复内容, 更新后的消息列表)
        """
        max_iterations = 10  # 防止无限循环
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            try:
                # Agent 决策
                if callback:
                    callback('thinking', f"第 {iteration} 轮思考...")
                
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=self.tools_schema,
                    stream=False
                )
                
                ai_message = response.choices[0].message
                
            except Exception as e:
                if callback:
                    callback('error', str(e))
                return f"API错误: {str(e)}", messages
            
            # 如果需要调用工具
            if ai_message.tool_calls:
                messages.append(ai_message.model_dump())
                
                # 遍历所有工具调用
                for tool_call in ai_message.tool_calls:
                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    if callback:
                        callback('tool_call', {
                            'name': func_name,
                            'args': args
                        })
                    
                    # 调用对应的工具函数
                    if func_name in self.tool_functions:
                        tool_result = self.tool_functions[func_name](**args)
                    else:
                        tool_result = f"未知工具: {func_name}"
                    
                    if callback:
                        callback('tool_result', {
                            'name': func_name,
                            'result': tool_result
                        })
                    
                    # 将工具结果添加到消息列表
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })
                
                # 继续下一轮循环，让模型根据工具结果生成回复
                continue
            
            # 如果模型返回了最终回复
            else:
                final_content = ai_message.content
                if callback:
                    callback('response', final_content)
                
                messages.append({
                    "role": "assistant",
                    "content": final_content
                })
                
                return final_content, messages
        
        # 超过最大迭代次数
        error_msg = "达到最大思考次数，请重新提问"
        if callback:
            callback('error', error_msg)
        return error_msg, messages
