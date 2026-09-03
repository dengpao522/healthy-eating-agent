from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender},帮我起个名字"
)

model = Tongyi(model = "qwen-max")

chain = prompt_template | model

res = chain.invoke(input={"lastname":"赵","gender":"女儿"})

print(res)