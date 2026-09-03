import jieba
from snownlp import SnowNLP

# 文本数据
texts = [
    '这部电影太棒了！',
    '这个产品很让人失望。',
    '今天天气真好。'
]

# 分词并计算文本情感强度
for text in texts:
    words = list(jieba.cut(text))
    s = SnowNLP(' '.join(words))
    sentiment_intensity = s.sentiments
    print(f'文本：{text}；情感强度：{sentiment_intensity}')