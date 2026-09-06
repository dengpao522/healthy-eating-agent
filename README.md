# 健康饮食助手

拍一张饭菜的照片，AI 帮你估算这顿饭的热量和三大营养素，再根据你的身高体重和运动习惯，算一下要运动多久才能消耗掉。

做这个的动机很简单：减脂期管不住嘴，又懒得每次吃完手动查每种菜的热量，干脆自己写一个。

## 它能做什么

- 上传饭菜照片，识别菜品并估算热量、碳水、蛋白质、脂肪。给的是区间值而不是精确数字，因为炒菜放了多少油模型判断不了，硬编一个精确值反而是骗人
- 按用户档案（身高体重年龄性别 + 运动等级）给"运动消耗参考"：散步要走多少步、跑步要跑几公里、打羽毛球要打多久
- 支持多轮对话，可以接着追问"那我中午少吃半碗米饭呢"
- 接了 Tavily 联网搜索，遇到模型不熟的菜品它会自己上网查

## 技术栈

- 后端：Python + FastAPI
- Agent：LangGraph 的 create_react_agent（ReAct 模式）
- 模型：通义千问 qwen-vl-max，走 OpenAI 兼容接口。选它是因为能看图，而且阿里百炼的接口直接兼容 OpenAI SDK，接起来省事
- 联网搜索：Tavily
- 图片存储：阿里云 OSS，前端拿预签名 URL 直传，图片不过我的服务器
- 前端：原生 HTML/CSS/JS，没用框架，够用

## 怎么跑起来

需要 Python 3.13+。

```bash
pip install fastapi uvicorn langgraph langchain-openai langchain-tavily python-dotenv alibabacloud-oss-v2
```

在 `app/agents/` 目录下建一个 `.env`：

```
OPENAI_BASE_URL=你的模型接口地址
OPENAI_API_KEY=你的key
TAVILY_API_KEY=你的tavily key
OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com
OSS_BUCKET=你的bucket名
OSS_ACCESS_KEY_ID=你的ak
OSS_ACCESS_KEY_SECRET=你的sk
```

启动：

```bash
python -m app.main
```

浏览器打开 http://127.0.0.1:8001 就能用了。

## 项目结构

```
app/
├── main.py                # FastAPI 入口，挂路由和静态页面
├── agents/
│   └── Healthy_eating.py  # Agent 核心：模型、系统提示词、流式输出
├── api/v1/
│   ├── chat.py            # 对话接口（SSE 流式）+ 历史消息
│   └── oss.py             # OSS 预签名 URL
├── models/schemas.py      # 请求参数定义
├── common/logger.py       # 日志
└── static/                # 前端页面
```

## 踩过的坑

记几个印象比较深的：

1. **.env 加载顺序**。oss.py 在模块顶层就创建了 OSS 客户端，如果 load_dotenv 在它 import 之后才执行，环境变量全是 None，而且报错位置离原因很远，排查了挺久。最后把 load_dotenv 挪到所有 import 之前才解决。

2. **Windows 编码问题**。单独跑 agent 脚本测图片识别，一输出中文就 UnicodeEncodeError，加了一行 `PYTHONUTF8=1` 才正常。

3. **从同步改成流式**。最早用的是 agent.invoke，用户发消息后页面空白十几秒等结果，体验很差。后来改成 astream + SSE。有个细节：LangGraph 的 `stream_mode="messages"` 吐出来的是 (chunk, metadata) 元组，不过滤 AIMessageChunk 的话，工具调用的中间过程也会被推给前端。

4. **CORS**。同源部署其实用不到，但之后打算做浏览器插件版（对着外卖页面拍照直接分析），所以先把中间件配上了。

## 已知不足 / TODO

- [ ] 会话历史存在内存里（MemorySaver），服务一重启就没了，之后想换成 SQLite
- [ ] 营养估算全靠模型，没接食物营养数据库做校验，误差偏大
- [ ] pyproject.toml 的 dependencies 还没整理全，暂时先用上面的 pip install
- [ ] 前端是手写的，比较糙
- [ ] 浏览器插件版还没动工

## 免责声明

所有数值都是 AI 估算，误差不小，只能当参考，替代不了营养师。
