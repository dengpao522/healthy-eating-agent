from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

parser = StrOutputParser()
model = ChatTongyi(model = "qwen-max")
prompt = PromptTemplate.from_template(
    "我姓{lastname}，刚出生{gender},起名"
)
chain = prompt | model | parser | model |parser

res = chain.invoke({"lastname":"赵","gender":"女儿"})
print(res)
