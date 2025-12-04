"""知识库RAG工具"""
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings.dashscope import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


class RAGSystem:
    """RAG知识库系统"""
    
    def __init__(self, docx_path, api_key):
        """
        初始化RAG系统
        
        Args:
            docx_path: 文档路径
            api_key: DashScope API密钥
        """
        self.docx_path = docx_path
        self.api_key = api_key
        self.rag_chain = None
        self.error = None
        
    def initialize(self):
        """初始化知识库"""
        if not os.path.exists(self.docx_path):
            self.error = f"⚠️ 未找到文件: {self.docx_path}"
            return False
        
        try:
            # 1. 加载文档
            loader = Docx2txtLoader(self.docx_path)
            pages = loader.load()
            
            # 2. 分割文档
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=100
            )
            docs = text_splitter.split_documents(pages)
            
            # 3. 向量化并存入 FAISS
            embeddings = DashScopeEmbeddings(
                model="text-embedding-v2", 
                dashscope_api_key=self.api_key
            )
            vector_store = FAISS.from_documents(docs, embeddings)
            
            # 4. 构建检索链
            retriever = vector_store.as_retriever()
            llm = ChatTongyi(
                model_name="qwen-plus", 
                dashscope_api_key=self.api_key, 
                temperature=0
            )
            
            template = """
            请根据以下提供的上下文来回答问题。
            如果你在上下文中找不到答案，就根据你的知识库查找答案，不要试图编造答案。

            上下文:
            {context}

            问题:
            {question}

            答案:
            """
            prompt = ChatPromptTemplate.from_template(template)
            
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)
            
            self.rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )
            
            print(f"✅ 知识库加载完成！共 {len(docs)} 个文档块。")
            return True
            
        except Exception as e:
            self.error = str(e)
            print(f"知识库初始化失败: {e}")
            return False
    
    def query(self, question):
        """
        查询知识库
        
        Args:
            question: 查询问题
            
        Returns:
            str: 查询结果
        """
        if not self.rag_chain:
            return f"知识库不可用: {self.error}"
        
        try:
            result = self.rag_chain.invoke(question)
            return result
        except Exception as e:
            return f"检索出错: {e}"


# 全局RAG实例
_rag_instance = None


def init_rag_system(docx_path, api_key):
    """
    初始化全局RAG系统
    
    Args:
        docx_path: 文档路径
        api_key: API密钥
        
    Returns:
        tuple: (RAG实例, 错误信息)
    """
    global _rag_instance
    _rag_instance = RAGSystem(docx_path, api_key)
    success = _rag_instance.initialize()
    return _rag_instance if success else None, _rag_instance.error


def search_knowledge_base(query):
    """
    使用 LangChain RAG 检索知识库
    
    Args:
        query: 查询问题
        
    Returns:
        str: 检索结果
    """
    if not _rag_instance:
        return "知识库未初始化"
    
    print(f"🔍 [RAG] 正在检索: {query}")
    return _rag_instance.query(query)
