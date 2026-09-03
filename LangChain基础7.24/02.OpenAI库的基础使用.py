from openai import OpenAI

client = OpenAI(
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key = "sk-b265692ac117460593817c3c015de140"
)

response = client.chat.completions.create(
    model = "qwen-max",
    messages = [
        {"role":"system","content":"你是一个Python编程专家，并且不说废话简单回答"},
        {"role":"assistant","content":"好的，我是编程专家 "},
        {"role":"user","content":"如何使用OpenAI库进行API调用"}
    ]
)

print(response.choices[0].message.content)