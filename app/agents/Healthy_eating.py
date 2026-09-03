import os
import base64
from dotenv import load_dotenv
os.environ["PYTHONUTF8"] = "1"
# 1. 必须显式加载环境变量！(这是运行 .py 脚本不报错的关键)
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk
from app.common.logger import logger
from langgraph.prebuilt import create_react_agent

from langgraph.checkpoint.memory import MemorySaver

# 2. 定义模型 (使用兼容 OpenAI 的接口)
model = ChatOpenAI(
    model="qwen-vl-max",
    temperature=0,
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# 3. 定义工具 (使用最新版 Tavily)
web_search_tool = TavilySearch(
    max_results=5,
    topic="general",
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)

# 4. 初始化checkpointer
checkpointer = MemorySaver()

# 4. 定义系统提示词 (你之前写好的那段很棒的提示词)
system_prompt = """
你是专业的健身营养分析Agent。
输入：用户上传的饭菜照片识别结果，用户档案：身高、体重、年龄、性别、可选运动等级（久坐 / 偶尔运动 / 规律性运动）可选运动习惯（散步、广场舞、跑步、羽毛球、网球、乒乓球、健身 ），运动时长（每周1小时、7小时、14小时）

你的工作流程：
1. 根据识别到的菜品、食材、估算重量、用油量（少油 / 正常 / 重油），计算：总热量（kcal）、碳水（g）、蛋白质（g）、脂肪（g）。
不要给出单一精确数字，**必须输出 最小值-最可能值-最大值 的区间**，并且标注误差来源（主要是炒菜油脂分量无法精确判断）。
2. 根据用户档案计算瘦体重校正系数：
- 如果用户选择【久坐】：采用普通人群能耗模型
- 如果用户选择【偶尔运动】：轻度校正
- 如果用户选择【规律性运动】：上调瘦体重占比，降低运动时长与步数结果
3. 根据用户运动习惯输出运动的消耗参考： 例如：                                                                                                       
散步：需要步数、预估时长
跑步：需要公里数、预估时长
羽毛球：运动时长
4. 给出实操减脂优化建议：例如撇掉浮油、减少米饭分量等。
5. 免责声明：所有数值为AI估算，仅供健身参考，不能替代营养师诊断。

输出格式，严格使用下面结构：
【营养估算】
热量： xxx-xxx kcal（最优值 xxx）
碳水： xxx-xxx g
蛋白质： xxx-xxx g
脂肪： xxx-xxx g


【运动消耗参考（按你的身体模型计算）】
散步：约 XXXX 步，XX小时XX分钟
跑步：约 XX.X 公里，XX小时XX分钟
羽毛球：XX小时XX分钟

【优化小建议】
● 建议1
● 建议2

⚠️ 免责：本结果仅为估算，存在一定误差，仅供训练参考。

约束规则：
- 禁止输出医学结论，不要使用绝对化词语。
- 如果菜品识别模糊，主动加宽估算区间，明确告知不确定性升高。
- 语言简洁易懂，不要专业晦涩术语。
"""

# 5. 创建 Agent
agent = create_react_agent(
    model,
    tools=[web_search_tool],
    checkpointer=checkpointer,
    prompt=system_prompt
)

# 流式对话
async def search_recipes(prompt: str, image: str, thread_id: str):
    """调用agent搜索食谱"""
    logger.info(f"[用户]: {prompt}, image: {image}, thread_id: {thread_id}")
    try:
        if not image or image.strip() == "":
            message = HumanMessage(content=prompt)
        else:
            message = HumanMessage(content=[
                {"type": "image_url", "image_url": {"url": image}},
                {"type": "text", "text": prompt}
            ])

        stream = agent.astream(
            input={"messages": [message]},
            config={"configurable": {"thread_id": thread_id}},
            stream_mode="messages"
        )
        async for chunk, metadata in stream:
            if isinstance(chunk, AIMessageChunk) and chunk.content:
                yield chunk.content

    except Exception as e:
        logger.error(f"[错误]: {str(e)}")
        yield f"错误：{str(e)}"


# 清空会话
def clear_messages(thread_id: str):
    """清空会话"""
    logger.info(f"清空历史消息，thread_id: {thread_id}")
    checkpointer.delete_thread(thread_id)


# 会话历史
def get_messages(thread_id: str) -> list[dict[str, str]]:
    """获取会话历史"""
    logger.info(f"获取历史消息，thread_id: {thread_id}")

    # 根据 thread_id 查询 checkpoint
    checkpoint = checkpointer.get({"configurable": {"thread_id": thread_id}})

    # 如果不存在，返回空列表
    if not checkpoint:
        return []

    # 安全获取 messages
    channel_values = checkpoint.get("channel_values")
    if not channel_values:
        return []

    messages = channel_values.get("messages", [])
    if not messages:
        return []

    # 转换消息格式
    result = []
    for msg in messages:
        if not msg.content:
            continue

        if isinstance(msg, HumanMessage):
            result.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            result.append({"role": "assistant", "content": msg.content})

    return result








# # 6. 测试代码 (直接读取本地图片)
# if __name__ == "__main__":
#     # 确保你的 food.jpg 和这个脚本在同一个目录下，或者改为绝对路径
#     image_path = "food.jpg"
#
#     with open(image_path, "rb") as f:
#         image_data = base64.b64encode(f.read()).decode('utf-8')
#
#     multimodal_message = HumanMessage(content=[
#         {"type": "text", "text": "这是我的午饭，请帮我计算营养和运动建议"},
#         {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
#     ])
#
#     response = agent.invoke({"messages": [multimodal_message]})
#
#     # 打印最终结果
#     print(response['messages'][-1].content)