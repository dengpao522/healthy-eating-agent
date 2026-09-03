import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# 文本数据样本
texts = [
    '我喜欢吃苹果。',
    '我喜欢吃香蕉。',
    '我喜欢吃牛肉。',
    '我喜欢吃鸡肉。',
    '橙子很好吃。',
    '猪肉很好吃。',
    '苹果汁真甜。',
    '香蕉很便宜。',
    '牛肉很有营养。',
    '鸡肉含蛋白质。',
    '我不喜欢吃榴梿。',
    '葡萄是紫色的。'
]

# 分词处理
corpus = []
for text in texts:
    # 使用jieba进行中文分词
    tokens = list(jieba.cut(text))
    # 将分词结果以空格连接，形成文本向量化所需的格式
    corpus.append(' '.join(tokens))

# 使用TF-IDF向量器对文本进行向量化
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

# 使用k-means算法进行聚类，设置聚类数为3
kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(tfidf_matrix)

# 输出聚类结果
labels = kmeans.labels_
for i in range(len(texts)):
    print('文本：', texts[i])
    print('标签：', labels[i])