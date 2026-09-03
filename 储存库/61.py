import jieba
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

# 定义文本数据集
corpus = [
    "这是一篇关于NLP的文章",
    "文本数据预处理非常重要",
    "TF-IDF是一种常用的文本特征提取方法",
    "关键词提取可以帮助我们理解文本的主题",
    "文本分类是NLP中的重要任务之一"
]

# 分词
seg_corpus = []
for text in corpus:
    seg_text = ' '.join(jieba.cut(text))  # 使用jieba进行分词，并以空格连接
    seg_corpus.append(seg_text)

# 初始化CountVectorizer向量器
vectorizer = CountVectorizer()
# 生成词频矩阵
term_frequency_matrix = vectorizer.fit_transform(seg_corpus)

# 初始化TF-IDF转换器
tfidf_transformer = TfidfTransformer()
# 计算TF-IDF矩阵
tfidf_matrix = tfidf_transformer.fit_transform(term_frequency_matrix)

# 获取特征词列表
feature_names = vectorizer.get_feature_names_out()

# 输出每个文档的关键词
for i in range(len(corpus)):
    doc_keywords = []
    for j, feature in enumerate(feature_names):
        if tfidf_matrix[i, j] > 0:  # 如果TF-IDF值大于0，说明该词在文本中出现过
            doc_keywords.append((feature, tfidf_matrix[i, j]))
    doc_keywords.sort(key=lambda x: x[1], reverse=True)  # 按TF-IDF值降序排列关键词
    print("文档{}的关键词：".format(i+1))
    for keyword, tfidf in doc_keywords:
        print("{0} ({1:.4f})".format(keyword, tfidf))  # 输出关键词及其对应的TF-IDF值
    print()