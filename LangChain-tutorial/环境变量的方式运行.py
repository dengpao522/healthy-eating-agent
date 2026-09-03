from langchain_openai import ChatOpenAI
import os

print(os.environ['OPENAI_BASE_URL'])
print(os.environ['OPENAI_API_KEY'])
#调用对话模型
chat_model = ChatOpenAI(
    #必须要设置的三个参数
    model_name='qwen-max',
    base_url=os.environ['OPENAI_BASE_URL'],
    api_key=os.environ['OPENAI_API_KEY'],
)

#调用模型
response=chat_model.invoke('我能进阿里做AI工程师吗')

#查看响应文本
print(response)