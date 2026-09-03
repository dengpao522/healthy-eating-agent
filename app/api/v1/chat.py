from fastapi import APIRouter
from app.models.schemas import ChatRequest
from langchain_core.messages import HumanMessage
from app.agents.Healthy_eating import search_recipes,get_messages,clear_messages
from fastapi.responses import StreamingResponse
# ~/api/v1
router = APIRouter()

# 延迟导入 agent，避免启动时阻塞
def get_agent():
    from app.agents.Healthy_eating import agent
    return agent

# ~/api/v1/chat/stream
@router.post("/chat/stream")
async def chat_endpoint(request: ChatRequest):
    # """流式对话"""
    # agent = get_agent()
    #
    # content = [{"type": "text", "text": request.message}]
    # if request.image_url:
    #     content.append({"type": "image_url", "image_url": {"url": request.image_url}})
    #
    # message = HumanMessage(content=content)
    # response = agent.invoke({"messages": [message]})
    #
    # reply = response["messages"][-1].content
    # return {"reply": reply}


    return StreamingResponse(
        search_recipes(request.message, request.image_url, request.thread_id),
        media_type="text/event-stream"
    )

# ~/api/v1/chat/messages
@router.get("/chat/messages")
async def get_chat_messages(thread_id: str):
    """获取历史消息"""
    # return {"messages": [], "thread_id": thread_id}

    messages = get_messages(thread_id)
    return {"messages": messages}

# ~/api/v1/chat/messages
@router.delete("/chat/messages")
async def clear_chat_messages(thread_id: str):
    """清空历史消息"""
    # return {"status": "ok", "thread_id": thread_id}

    clear_messages(thread_id)
    return {"success": True}