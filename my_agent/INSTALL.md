# 安装指南

## 📦 安装步骤

### 第一步：复制数据文件

请将小米 YU7 的文档文件复制到 data 目录：

**方法1：手动复制**
1. 打开文件资源管理器
2. 从 `E:\Agent\AI助手\xiaomiYU7.docx` 复制文件
3. 粘贴到 `E:\Agent\my_agent\data\` 目录

**方法2：使用 PowerShell 命令**
```powershell
Copy-Item "E:\Agent\AI助手\xiaomiYU7.docx" -Destination "E:\Agent\my_agent\data\xiaomiYU7.docx"
```

### 第二步：配置环境变量

编辑 `.env` 文件，填入你的真实 API 密钥：

```env
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
AMAP_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**获取 API 密钥：**
- **DashScope API**: 访问 https://dashscope.aliyun.com/ 注册并获取
- **高德地图 API**: 访问 https://lbs.amap.com/ 注册并创建应用获取

### 第三步：安装 Python 依赖

使用项目配置的 Python 解释器安装依赖：

```powershell
E:\AI_Envs\ai_agent\python.exe -m pip install -r requirements.txt
```

或者如果使用系统 Python：

```powershell
pip install -r requirements.txt
```

### 第四步：运行应用

**方法1：使用启动脚本（推荐）**
```powershell
cd E:\Agent\my_agent
.\start.ps1
```

**方法2：直接运行**
```powershell
cd E:\Agent\my_agent
E:\AI_Envs\ai_agent\python.exe -m streamlit run app.py
```

或者：
```powershell
streamlit run app.py
```

## ✅ 验证安装

应用启动后，你应该看到：

1. 浏览器自动打开 `http://localhost:8501`
2. 页面显示 "🚗 小米 YU7 专属 AI 顾问 (Agent + RAG)"
3. 左侧边栏显示 "✅ 知识库已加载"

## 🐛 故障排除

### 问题1：ModuleNotFoundError: No module named 'docx2txt'

**解决方法：**
```powershell
pip install docx2txt
```

### 问题2：知识库初始化失败

**检查项：**
1. 确认 `data/xiaomiYU7.docx` 文件存在
2. 确认已安装 `docx2txt` 模块
3. 确认 DASHSCOPE_API_KEY 配置正确

### 问题3：天气/地图功能不可用

**检查项：**
1. 确认 `.env` 文件中配置了 `AMAP_KEY`
2. 确认 API 密钥有效且有剩余额度

### 问题4：端口占用

如果 8501 端口被占用，可以指定其他端口：

```powershell
streamlit run app.py --server.port 8502
```

## 📚 依赖说明

核心依赖包：
- `streamlit`: Web 界面框架
- `openai`: OpenAI 兼容接口
- `langchain`: RAG 框架
- `docx2txt`: DOCX 文档解析
- `faiss-cpu`: 向量检索
- `python-dotenv`: 环境变量管理

## 🔄 更新知识库

如果需要更新知识库文档：

1. 替换 `data/xiaomiYU7.docx` 文件
2. 清除 Streamlit 缓存：在浏览器中按 `C` 键
3. 刷新页面，系统会重新加载知识库

## 💡 使用技巧

1. **首次启动**：首次运行需要加载和向量化文档，需要等待约 10-30 秒
2. **缓存机制**：知识库会被缓存，后续刷新页面不会重新加载
3. **清空对话**：点击左侧边栏的 "🗑️ 清空对话历史" 按钮
4. **查看日志**：终端会显示工具调用的日志信息
