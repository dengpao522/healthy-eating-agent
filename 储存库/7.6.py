from gensim.models import Word2Vec
import jieba

# 中文语料
text = """
我喜欢吃苹果。
他们去公园玩得很开心。
她读了一本很有趣的书。
我在学习机器学习的课程。
这个问题很复杂，需要认真思考。
"""

# 分词
tokens = list(jieba.cut(text))

# 构建训练数据
data = [tokens]

# 训练Skip-Gram模型
model = Word2Vec(sentences=data, window=5, vector_size=100, sg=1, min_count=1, workers=4)

# 获取词向量
embedding_weights = model.wv

# 输出词向量
for word in embedding_weights.index_to_key:
    print(word, embedding_weights[word])