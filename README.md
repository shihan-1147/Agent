小米 YU7 智能助手 (Agent + RAG)
基于 ReAct 架构的 AI Agent，集成知识库检索（RAG）、天气查询和地图搜索功能。

📁 项目结构
my_agent/
├── .env                    # 环境变量配置（API密钥）
├── app.py                  # Streamlit 界面渲染
├── agent_core.py           # ReAct 循环核心逻辑
├── requirements.txt        # Python 依赖包
├── tools/                  # 工具函数模块
│   ├── __init__.py        # 工具包初始化
│   ├── weather.py         # 天气查询函数
│   ├── map.py             # 地图搜索函数
│   └── rag.py             # 知识库 RAG 函数
└── data/
    └── xiaomiYU7.docx     # 知识库文档
🚀 快速开始
1. 安装依赖
cd E:\Agent\my_agent
pip install -r requirements.txt
2. 配置环境变量
编辑 .env 文件，填入你的 API 密钥：

DASHSCOPE_API_KEY=your_dashscope_api_key_here
AMAP_KEY=your_amap_key_here
3. 准备数据文件
将小米 YU7 的文档文件放到 data/xiaomiYU7.docx

4. 运行应用
streamlit run app.py
🛠️ 功能模块说明
Agent 核心 (agent_core.py)
AgentCore 类: 实现 ReAct 循环逻辑
run_agent 方法: 执行多轮对话和工具调用
回调机制: 支持 UI 实时更新
工具模块 (tools/)
1. 知识库检索 (rag.py)
基于 LangChain 的 RAG 系统
支持 DOCX 文档加载和向量化
使用 FAISS 进行向量检索
2. 天气查询 (weather.py)
调用高德地图天气 API
返回指定城市的实时天气信息
3. 地图搜索 (map.py)
调用高德地图地点搜索 API
支持关键词和城市搜索
界面模块 (app.py)
Streamlit 聊天界面
会话状态管理
实时状态显示
打字机效果输出
📋 使用示例
查询车辆信息
用户: YU7 的续航里程是多少？
助手: [调用 search_knowledge_base] 根据文档，小米 YU7...
查询天气
用户: 北京今天天气怎么样？
助手: [调用 get_weather] 北京 天气晴 15℃
搜索地点
用户: 帮我找一下上海的小米之家
助手: [调用 search_nearby] 1. 小米之家 - 南京东路xxx号...
🔧 扩展开发
添加新工具
在 tools/ 目录下创建新的工具文件
在 tools/__init__.py 中导出函数
在 agent_core.py 中添加工具描述和函数映射
示例：

# tools/calculator.py
def calculate(expression):
    """计算数学表达式"""
    return eval(expression)

# agent_core.py
TOOLS_SCHEMA.append({
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "计算数学表达式",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string"}
            },
            "required": ["expression"]
        }
    }
})
📝 注意事项
确保已安装 docx2txt 模块，否则知识库无法初始化
API 密钥必须通过环境变量配置，不要硬编码
首次运行会进行向量化，需要一些时间
知识库会使用 @st.cache_resource 缓存，刷新页面不会重新加载
🐛 常见问题
Q: 知识库加载失败？
A: 检查 data/xiaomiYU7.docx 是否存在，确保已安装 docx2txt

Q: 天气和地图功能不可用？
A: 检查 .env 文件中是否正确配置了 AMAP_KEY

Q: Agent 不调用工具？
A: 检查 system prompt 是否正确引导模型调用工具

📄 许可证
MIT License
