"""Streamlit界面 - 小米YU7智能助手"""
import streamlit as st
import os
import time
from dotenv import load_dotenv
from agent_core import AgentCore
from tools.rag import init_rag_system
import uuid
import history_utils  # ✨ 导入历史记录工具

# 加载环境变量
load_dotenv()

# ============ 1. 页面配置 ============
st.set_page_config(page_title="小米 YU7 知识助手", page_icon="🚗", layout="wide")  # ✨ layout="wide" 让侧边栏更舒服

# ============ 1.5 自定义CSS样式 - ChatGPT风格居中布局 ============
st.markdown("""
<style>
    /* 主容器居中 */
    .main .block-container {
        max-width: 200px;
        padding-left: 2rem;
        padding-right: 2rem;
        margin: 0 auto;
    }
    
    /* 聊天消息容器样式优化 */
    .stChatMessage {
        max-width: 100%;
        margin: 0 auto 1rem auto;
    }
    
    /* 用户消息样式 */
    .stChatMessage[data-testid="user-message"] {
        background-color: #2b2b2b;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* 助手消息样式 */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #1e1e1e;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* 输入框容器 */
    .stChatInputContainer {
        max-width: 200px;
        margin: 0 auto;
        padding: 1rem 0;
    }
    
    /* 标题居中 */
    h1 {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* 优化聊天输入框样式 */
    .stChatInput {
        border-radius: 24px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚗 小米 YU7 专属 AI 顾问 (Agent + RAG)")

# 获取 API Keys
API_KEY = os.getenv('DASHSCOPE_API_KEY')
AMAP_KEY = os.getenv('AMAP_KEY')

if not API_KEY:
    st.error("请在 .env 文件中设置 DASHSCOPE_API_KEY！")
    st.stop()

if not AMAP_KEY:
    st.warning("未设置 AMAP_KEY 环境变量，地图与天气功能将不可用。")


# ============ 2. 初始化 RAG 系统 ============
@st.cache_resource
def initialize_rag():
    """初始化RAG知识库"""
    # 确保你的路径是正确的
    docx_path = os.path.join(os.path.dirname(__file__), "data", "xiaomiYU7.docx")

    status_container = st.empty()
    status_container.info("🔄 正在初始化知识库 (加载 docx -> 向量化)...")

    # 注意：这里的传参要和你 tools/rag.py 里的定义一致
    rag_instance, error = init_rag_system(docx_path, API_KEY)

    if rag_instance:
        status_container.success("✅ 知识库加载完成！")
        time.sleep(1)
        status_container.empty()
    else:
        status_container.error(f"⚠️ 知识库初始化失败: {error}")

    return rag_instance, error


rag_instance, rag_error = initialize_rag()


# ============ 3. 初始化 Agent ============
@st.cache_resource
def get_agent():
    """获取Agent实例"""
    return AgentCore(api_key=API_KEY)


agent = get_agent()

# ============ 4. 会话状态管理 (✨ 核心修改) ============

# 初始化当前的 Chat ID
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())

# 初始化消息列表
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "你是一个小米汽车的智能顾问。关于车辆的具体配置问题，请务必调用 search_knowledge_base 工具查询知识库。关于生活服务问题，调用地图或天气工具。"
        }
    ]

# ============ 5. 侧边栏：历史记录 (✨ 新增模块) ============
with st.sidebar:
    st.header("🗂️ 对话管理")

    # A. 新建对话按钮
    if st.button("➕ 新建对话", use_container_width=True):
        st.session_state.current_chat_id = str(uuid.uuid4())
        st.session_state.messages = [
            {"role": "system",
             "content": "你是一个小米汽车的智能顾问。关于车辆的具体配置问题，请务必调用 search_knowledge_base 工具查询知识库。关于生活服务问题，调用地图或天气工具。"}
        ]
        st.rerun()

    st.divider()

    # B. 显示历史列表
    st.subheader("历史记录")
    history_list = history_utils.get_all_conversations()

    for chat in history_list:
        # 给每个按钮唯一的 Key
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            # 选中当前对话时高亮显示 (通过 emoji 区分)
            label = f"💬 {chat['title']}"
            if chat['id'] == st.session_state.current_chat_id:
                label = f"🟢 {chat['title']}"

            if st.button(label, key=f"btn_{chat['id']}", use_container_width=True):
                st.session_state.current_chat_id = chat['id']
                st.session_state.messages = history_utils.load_conversation(chat['id'])
                st.rerun()
        with col2:
            # 删除按钮
            if st.button("✖️", key=f"del_{chat['id']}", help="删除此记录"):
                history_utils.delete_conversation(chat['id'])
                # 如果删的是当前对话，重置
                if chat['id'] == st.session_state.current_chat_id:
                    st.session_state.current_chat_id = str(uuid.uuid4())
                    st.session_state.messages = [{"role": "system", "content": "你是一个小米汽车的智能顾问。"}]
                st.rerun()

    # 原来的系统信息挪到底部
    st.divider()
    with st.expander("ℹ️ 系统状态"):
        st.info(f"""
        **API:** {'✅' if API_KEY else '❌'}
        **RAG:** {'✅' if rag_instance else '❌'}
        **Chat ID:** `{st.session_state.current_chat_id[:8]}...`
        """)

# ============ 6. 渲染当前聊天内容 ============
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant" and msg.get("content"):
        st.chat_message("assistant").write(msg["content"])

# ============ 7. 处理用户输入 & 自动保存 (✨ 修改部分) ============
if prompt := st.chat_input("请问关于小米 YU7 的问题..."):
    # 显示用户消息
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # ✨ 1. 用户输入完，立即保存一次 (防止还没回答就断了)
    history_utils.save_conversation(st.session_state.current_chat_id, st.session_state.messages)

    # 显示助手回复区域
    with st.chat_message("assistant"):
        status_container = st.status("🤖 AI 正在思考...", expanded=True)
        response_placeholder = st.empty()
        full_response = ""


        # 回调函数
        def agent_callback(event_type, data):
            if event_type == 'thinking':
                status_container.update(label=f"🤔 {data}", state="running")
            elif event_type == 'tool_call':
                status_container.write(f"🔧 正在调用工具：**{data['name']}**")
                if data['name'] == 'search_knowledge_base':
                    status_container.write(f"📖 正在翻阅文档: {data['args'].get('query', '')}")
            elif event_type == 'tool_result':
                result_preview = str(data['result'])[:100]
                status_container.write(f"✓ {data['name']} 完成")
            elif event_type == 'response':
                status_container.update(label="✨ 回答生成完成", state="complete", expanded=False)
            elif event_type == 'error':
                status_container.error(f"❌ 错误: {data}")


        # 运行 Agent
        final_response, updated_messages = agent.run_agent(
            messages=st.session_state.messages.copy(),
            callback=agent_callback
        )

        # 更新会话状态
        st.session_state.messages = updated_messages

        # 打字机效果
        for char in final_response:
            full_response += char
            response_placeholder.markdown(full_response + "▌")
            time.sleep(0.01)

        response_placeholder.markdown(full_response)

        # ✨ 2. AI 回答完，再次保存完整对话
        # 注意：AgentCore 可能会返回新的 messages 列表（包含 tool calls），我们要保存这个完整的
        history_utils.save_conversation(st.session_state.current_chat_id, st.session_state.messages)