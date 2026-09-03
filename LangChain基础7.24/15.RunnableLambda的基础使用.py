from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

str_parser = StrOutputParser()
model = ChatTongyi(model = "qwen-max")
first_prompt = PromptTemplate.from_template(
    "我姓{lastname}，刚出生{gender},起名"
)
second_prompt = PromptTemplate.from_template(
    "姓名：{name},帮我解析含义"
)

my_func = RunnableLambda(lambda ai_msg: {"name":ai_msg.content})

chain = first_prompt | model | my_func | second_prompt | model | str_parser


res = chain.invoke({"lastname":"赵","gender":"女儿"})
print(res)