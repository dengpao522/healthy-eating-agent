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

# 指定词向量的维度
vector_size = 50

# 训练CBOW模型
model = Word2Vec(sentences=data, window=2, min_count=1, sg=0, vector_size=vector_size, workers=4)

# 参数说明如下
# sentences：训练数据，一个二维列表，每个内部列表表示一个句子的分词结果
# window：滑动窗口大小（窗口大小），控制上下文词的范围
# min_count：最小词频阈值（最小词频），低于该阈值的词将被忽略
# sg：选择被训练的模型，0表示使用CBOW模型，1表示使用Skip-Gram模型
# vector_size：词向量的维度（向量维度）
# workers：并行化训练时的线程数

# 获取词向量
embedding_weights = model.wv

# 输出词向量
for word in embedding_weights.index_to_key:
    print(word, embedding_weights[word])