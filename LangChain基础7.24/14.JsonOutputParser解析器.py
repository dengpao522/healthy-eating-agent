from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

parser = StrOutputParser()
model = ChatTongyi(model = "qwen-max")
first_prompt = PromptTemplate.from_template(
    "我姓{lastname}，刚出生{gender},起名"
    "并封装为JSON格式，要求key是name,value是你起的名字 "
)

second_prompt = PromptTemplate.from_template(
    "姓名：{name},帮我解析含义"
)

chain = first_prompt | model | json_parser | second_prompt | model | str_parser

for chunk in chain.stream({"lastname":"赵","gender":"女儿"}):
    print(chunk,end="",flush = True)