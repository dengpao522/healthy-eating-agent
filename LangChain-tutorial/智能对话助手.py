import os
from langchain_community.tools import TavilySearchResults
import json

from langchain_core.tools import create_retriever_tool

os.environ['TAVILY_API_KEY'] = "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"
os.environ['DASHSCOPE_API_KEY'] = "sk-b265692ac117460593817c3c015de140"
search_tool = TavilySearchResults(max_results=3)
# result = search_tool.invoke("查询今天北京的天气情况")
# print(result)


from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


import dotenv

dotenv.load_dotenv()

# 1. 提供一个大模型（使用阿里云 DashScope Embeddings）
embedding_model = DashScopeEmbeddings(
    model="text-embedding-v1",  # 阿里云通义千问的 embedding 模型
)

# 2. 加载HTML内容为一个文档对象
loader = WebBaseLoader("https://mybatis.org/mybatis-3/zh_CN/getting-started.html")
docs = loader.load()
#print(docs)

# 3. 分割文档
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

documents = splitter.split_documents(docs)

# 4.向量化 得到向量数据库对象
vector = FAISS.from_documents(documents, embedding_model)

# 5.创建检索器
retriever = vector.as_retriever()

# 测试检索结果
print(retriever.invoke("作用域和生命周期")[0])

# 创建一个工具来检索文档
retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="wiki_search",
    description="中国百科网",
)

# 构建工具集
tools = [search_tool, retriever_tool]


