import jieba

# 情感词典（包含积极情感词和消极情感词）
positive_words = ['喜欢', '愉快', '赞美', '好']
negative_words = ['讨厌', '悲伤', '垃圾', '坏']

def sentiment_analysis(text):
    # 分词
    words = jieba.lcut(text)
    # 初始化情感得分
    sentiment_score = 0
    # 遍历每个词
    for word in words:
        if word in positive_words:
            sentiment_score += 1  # 积极情感词得分加1
        elif word in negative_words:
            sentiment_score -= 1  # 消极情感词得分减1
    # 根据情感得分判断情感极性
    if sentiment_score > 0:
        sentiment = '积极'
    elif sentiment_score < 0:
        sentiment = '消极'
    else:
        sentiment = '中性'
    return sentiment

# 测试文本
text = '这部电影太好看了，赞美一下！'
result = sentiment_analysis(text)
print('情感极性：', result)

text = '这家餐厅的服务太差了，讨厌！'
result = sentiment_analysis(text)
print('情感极性：', result)