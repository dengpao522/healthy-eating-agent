from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","你是诗人"),
        MessagesPlaceholder("history"),
        ("human","再来一首"),
    ]
)

history_data = [
    ("human","来首诗"),
    ("ai","床前明月光..."),
    ("human","再来一首"),
    ("ai","锄禾日当午..."),
]

prompt_text = chat_prompt_template.invoke({"history":history_data}).to_string()

model = ChatTongyi(model = "qwen-max")

response = model.invoke(prompt_text)
print(response.content,type(response))



