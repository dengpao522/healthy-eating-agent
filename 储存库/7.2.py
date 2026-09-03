import jieba
from sklearn.feature_extraction.text import CountVectorizer

# 准备数据
sentences = ['我喜欢吃苹果。', '他喜欢吃香蕉。', '我喜欢吃橙子。']

# 分词
tokenized_sentences = [' '.join(jieba.lcut(sentence)) for sentence in sentences]

# 创建BoW模型
vectorizer = CountVectorizer()

# 文本向量化
X = vectorizer.fit_transform(tokenized_sentences)

# 输出特征词
features = vectorizer.get_feature_names_out()
print("特征词：", features)

# 输出文本向量
print("文本向量：")
for i, sentence in enumerate(sentences):
    print(f"句子{i+1}：{sentence}")
    print(X[i].toarray())
    print()