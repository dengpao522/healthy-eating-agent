from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

model = ChatTongyi(model = "qwen-max")

messages = [
    HumanMessage(content = "介绍一下安赛龙")
]

res = model.stream(input = messages)

for chunk in res:
    print(chunk.content,end = "",flush = True)