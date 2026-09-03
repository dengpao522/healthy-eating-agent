import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD

# 文本数据预处理函数
def preprocess_text(text):
    """
    对文本进行分词和过滤停用词
    参数: 待处理的文本
    返回值: 处理后的文本
    """
    # 使用jieba进行分词
    seg_list = jieba.lcut(text)
    # 停用词列表
    stopwords = set(['的', '了', '是', '我', '你', '他'])
    # 过滤停用词和单个字的词
    seg_list = [word for word in seg_list if word not in stopwords and len(word) > 1]
    # 返回分词后的结果
    return " ".join(seg_list)

# 构建语料库
corpus = [
    "这是一篇关于机器学习的文章",
    "机器学习是人工智能的一个重要领域",
    "人工智能正在改变我们的生活",
    "机器学习的应用非常广泛",
    "人工智能会带来技术革命"
]

# 对每篇文档进行预处理
processed_corpus = [preprocess_text(text) for text in corpus]

# 构建词-文档矩阵
vectorizer = CountVectorizer()
tf_matrix = vectorizer.fit_transform(processed_corpus)

# 使用LSA算法进行降维
svd = TruncatedSVD(n_components=2)
lsa_matrix = svd.fit_transform(tf_matrix)

# 输出关键词
features = vectorizer.get_feature_names_out()
for i, component in enumerate(svd.components_):
    feature_idx = component.argsort()[::-1][:5]  # 取前5个关键词
    keywords = [features[idx] for idx in feature_idx]
    print(f"第{i+1}个主题的关键词：", keywords)