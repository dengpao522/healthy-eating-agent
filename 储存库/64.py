import jieba
from gensim import corpora, models

# 文本数据预处理函数
def preprocess(texts):
    """
    对文本进行预处理，包括分词和去除停用词
    参数: 待处理的文本列表
    返回值: 处理后的文本列表
    """
    processed_texts = []
    for text in texts:
        # 分词、去除停用词等操作
        words = [word for word in jieba.cut(text) if word.strip() != '' and word not in stop_words]
        processed_texts.append(words)
    return processed_texts

# 构建词典和文档-词矩阵
def build_corpus(processed_texts):
    """
    根据处理后的文本构建词典和文档-词矩阵
    参数如下
    processed_texts: 处理后的文本列表
    返回值如下
    dictionary: 字典对象，将词映射为整数ID
    corpus: 文档-词矩阵，以稀疏向量表示每个文档中词出现的次数
    """
    dictionary = corpora.Dictionary(processed_texts)  # 构建字典
    corpus = [dictionary.doc2bow(text) for text in processed_texts]  # 将文本转换为稀疏向量
    return dictionary, corpus

# 使用LDA算法训练模型并提取关键词
def get_keywords(texts, num_topics=5, num_words=5, passes=10):
    """
    使用LDA算法训练模型，并提取每个主题的关键词
    参数如下
    texts: 文本列表
    num_topics: 主题数量，默认为5
    num_words: 每个主题提取的关键词数量，默认为5
    passes: LDA算法迭代次数，默认为10
    返回值如下
    keywords_list: 每个主题的关键词列表
    """
    # 文本数据预处理
    processed_texts = preprocess(texts)
    # 构建BoW模型
    dictionary, corpus = build_corpus(processed_texts)
    # 使用LDA算法训练模型
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
    # 提取关键词
    keywords_list = []
    for i in range(num_topics):
        topic_keywords = lda_model.show_topic(i, topn=num_words)
        keywords = [keyword for keyword, _ in topic_keywords]
        keywords_list.append(keywords)
    return keywords_list

# 示例文本数据
texts = [
    "这个产品很好用",
    "这款手机拍照效果很出色",
    "这本书的故事情节很精彩",
    "这个电视的画质非常清晰",
    "这个酒店的服务态度很好"
]

# 停用词列表，可以根据实际需求添加
stop_words = []

# 调用函数提取关键词
keywords_list = get_keywords(texts)

# 输出结果
for i, keywords in enumerate(keywords_list):
    print("第{}个主题的关键词：".format(i+1))
    print(keywords)
    print()