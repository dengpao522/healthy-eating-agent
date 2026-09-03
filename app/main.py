import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# 加载环境变量（必须在导入 oss 之前）
env_path = os.path.join(os.path.dirname(__file__), "agents", ".env")
load_dotenv(env_path, override=True)

from app.common.logger import setup_logging
from app.api.v1 import chat, oss

# 初始化日志配置
setup_logging()

app = FastAPI(
    title="Personal Chief API",
    description="健康饮食",
    version="0.1.0"
)

# 1. 配置跨域资源共享（CORS）
# 插件开发中，由于请求来自浏览器扩展环境，必须正确配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定插件的 ID 或具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 挂载路由
# ~/api/v1
app.include_router(chat.router, prefix="/api/v1", tags=["对话"])
# ~/api/v1
app.include_router(oss.router, prefix="/api/v1", tags=["申请上传签名url"])

# 3. 挂载前端资源
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

# 前端 fallback 路由 - 只处理非 API 请求
# ~/[path:path]
@app.get(path="/{path:path}", include_in_schema=False)
async def serve_frontend(path: str):
    # 排除 API 路径
    if path.startswith("api/"):
        from fastapi.responses import JSONResponse
        return JSONResponse(content={"error": "Not Found"}, status_code=404)
    # 如果请求的是静态文件，直接返回
    file_path = os.path.join(static_dir, path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    # 否则返回 index.html（SPA fallback）
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "你的健康饮食管家上线了~", "status": "ok"}

if __name__ == "__main__":
    import uvicorn
    # 启动命令：python -m app.main
    uvicorn.run(app="app.main:app", host="127.0.0.1", port=8001, reload=True)