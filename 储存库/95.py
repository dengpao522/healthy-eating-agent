from snownlp import SnowNLP
import matplotlib.pyplot as plt
import pandas as pd

# 中文文本数据
texts = [
    "今天心情很好，工作顺利",
    "周一了，不想上班啊",
    "开心的事情真是太少了",
    "听说明天要下雨，有点烦"
]

# 初始化情感分析结果列表
sentiments_sn = []

# 使用snownlp库对每个文本进行情感分析
for text in texts:
    # 使用SnowNLP计算情感得分，范围为0（负面）~1（正面）
    sn = SnowNLP(text)
    sentiments_sn.append(sn.sentiments)

# 创建DataFrame
df = pd.DataFrame({
    'Text': texts,
    'Sentiment_SN': sentiments_sn  # 存储使用SnowNLP分析得到的情感分析结果
})

# 输出情感分析结果
print(df)

# 绘制情感时序分析图
plt.figure(figsize=(10, 6), dpi=600)
plt.rcParams['font.family'] = ['SimHei']  # 解决中文显示问题
plt.plot(df['Sentiment_SN'], marker='x', label='SnowNLP')
plt.xticks(ticks=range(len(df['Text'])), labels=df['Text'], rotation=45)
plt.xlabel('文本', fontsize=14)
plt.ylabel('情感得分', fontsize=14)
plt.title('情感时序分析', fontsize=16)
plt.legend()
plt.show()