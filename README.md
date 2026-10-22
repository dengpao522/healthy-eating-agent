> [!NOTE]
> **本项目已演进为 [health-app-pro（健康饮食 Agent Pro）](https://github.com/dengpao522/health-app-pro)**
> 在本项目的 Agent 链路基础上，完成了产品化重构：507 条食物库、分类营养评分引擎、轻断食/生理期/周报等 30+ 功能、39 个自动化测试 + CI。
> 本仓库保留为 **Agent 1.0 原型**（LangGraph 编排思路的来源），不再积极开发。

# 健康饮食助手

拍一张饭菜的照片，AI 帮你估算这顿饭的热量和三大营养素，再根据你的身高体重和运动习惯，算一下要运动多久才能消耗掉。

做这个的动机很简单：减脂期管不住嘴，又懒得每次吃完手动查每种菜的热量，干脆自己写一个。项目重点在 Agent 这一层，前后端只是搭了个能用的壳。

## 它能做什么

- 上传饭菜照片，识别菜品并估算热量、碳水、蛋白质、脂肪
- 按用户档案（身高体重年龄性别 + 运动等级）给"运动消耗参考"：散步要走多少步、跑步要跑几公里、打羽毛球要打多久
- 多轮对话，可以接着追问"那我中午少吃半碗米饭呢"
- 遇到模型不熟的菜品，会调联网搜索自己查资料

## Agent 部分（项目的重点）

整体流程：用户上传图片 → 前端拿 OSS 预签名 URL 直传 → 把图片 URL 和文字包进一条多模态消息发给 Agent → Agent 分析后流式返回。

### 为什么用 create_react_agent

一开始跟着教程手写过"模型输出 → 判断要不要调工具 → 手动执行 → 拼回消息"的循环，能跑但代码很散。后来换成 LangGraph 的 create_react_agent，工具调用、中间状态、循环终止这些都由框架管，我只需要关心三件事：模型、工具、提示词。代码从一百来行缩到几十行，还白得了一个 checkpoint 机制。

```python
agent = create_react_agent(
    model,                    # 通义千问 qwen-vl-max，OpenAI 兼容接口
    tools=[web_search_tool],  # Tavily 联网搜索
    checkpointer=checkpointer,
    prompt=system_prompt
)
```

### 系统提示词是花时间最多的地方

这个项目的效果好坏基本取决于提示词，我反复调过几版，几个关键设计：

**1. 热量必须给区间，不给精确值。** 最早的版本模型会输出"这顿饭 658 kcal"，看着很专业，其实是瞎编的精度——炒菜放了多少油模型根本判断不了。现在强制输出"最小值-最可能值-最大值"，并要求标注误差来源。还加了一条约束：菜品识别模糊时主动加宽区间、告知不确定性升高。

**2. 不同运动水平用不同的算法。** 用户选"久坐 / 偶尔运动 / 规律性运动"，提示词里分别对应普通人群能耗模型、轻度校正、上调瘦体重占比三种处理方式。同一个饭量给久坐的人和健身的人算出来的消耗是不一样的。

**3. 把"消耗"换算成可执行的动作。** 不说"你需要消耗 300 kcal"这种废话，而是直接给"跑步 4 公里约 40 分钟""散步 8000 步"，用户看完就知道该干嘛。

**4. 兜底约束。** 禁止输出医学结论、禁止绝对化表述、输出末尾固定带免责声明——怕它给人算出一身病。

### 工具调用

只挂了一个 Tavily 搜索。设计思路是让 Agent 自己决定什么时候搜：家常菜它自己能估，遇到小众菜品（比如某个地方菜）搜索结果能明显减少瞎编。

### 会话记忆

用 LangGraph 的 MemorySaver 做 checkpoint，前端给每个会话生成一个 thread_id，追问"少吃半碗米饭呢"这种上下文问题就能接住。另外补了两个接口：按 thread_id 拉历史消息、清空会话（对应页面上"新建对话"和"清空当前对话"按钮）。

### 从同步改成流式（体验上最大的提升）

最早用 agent.invoke，用户发完消息盯着空白页面等十几秒。改成 `astream` + SSE 之后，字是一个一个蹦出来的。

一个细节：`stream_mode="messages"` 吐出来的是 `(chunk, metadata)` 元组，不过滤 `AIMessageChunk` 的话，工具调用的中间过程（比如"正在调用 Tavily"）也会被当成回答推给前端。调试的时候才发现这个问题。

## 其他部分

后端 FastAPI 起了个 `/api/v1/chat/stream`（SSE）加历史消息接口，图片走阿里云 OSS 预签名 URL 直传，不占服务器带宽。前端是原生 JS 写的聊天页。这两块不是项目重点，就不展开了。

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

1. **.env 加载顺序**。oss.py 在模块顶层就创建了 OSS 客户端，如果 load_dotenv 在它 import 之后才执行，环境变量全是 None，而且报错位置离原因很远。最后把 load_dotenv 挪到所有 import 之前才解决。

2. **Windows 编码问题**。单独跑 agent 脚本测图片识别，一输出中文就 UnicodeEncodeError，加了一行 `PYTHONUTF8=1` 才正常。

3. **流式输出的垃圾内容**。就是上面说的 AIMessageChunk 过滤问题，前端一度把"正在调用搜索工具"这种中间态直接显示给用户。

## 已知不足 / TODO

- [ ] 会话历史存在内存里（MemorySaver），服务一重启就没了，之后想换成 SQLite
- [ ] 营养估算全靠模型，没接食物营养数据库做校验，误差偏大
- [ ] 只有一个搜索工具，之后想加一个"查询食物数据库"的自定义工具试试多工具路由
- [ ] pyproject.toml 的 dependencies 还没整理全，暂时先用上面的 pip install
- [ ] 浏览器插件版还没动工

## 免责声明

所有数值都是 AI 估算，误差不小，只能当参考，替代不了营养师。
