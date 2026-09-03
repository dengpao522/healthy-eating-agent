import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# 训练数据样本
train_data = [
    {'text': '我喜欢吃苹果。', 'label': '水果'},
    {'text': '香蕉是黄色的水果。', 'label': '水果'},
    {'text': '梨子和苹果都很甜。', 'label': '水果'},
    {'text': '草莓是红色的。', 'label': '水果'},
    {'text': '我喜欢吃牛肉。', 'label': '肉类'},
    {'text': '鸡肉含有丰富的蛋白质。', 'label': '肉类'},
    {'text': '猪肉是红肉的一种。', 'label': '肉类'},
    {'text': '羊肉炖着吃很美味。', 'label': '肉类'}
]

# 测试数据样本
test_data = [
    {'text': '我喜欢吃橙子。'},
    {'text': '我喜欢吃猪肉。'}
]

# 使用jieba对文本进行分词处理
def tokenize(text):
    return list(jieba.cut(text))

# 对训练数据样本和测试数据样本进行分词
for data in train_data + test_data:
    data['tokens'] = tokenize(data['text'])

# 构建语料库，只使用训练数据样本
corpus = [data['text'] for data in train_data]

# 初始化TF-IDF向量化器，并将文本转换为TF-IDF特征矩阵
tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenize)
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

# 训练朴素贝叶斯分类器
clf = MultinomialNB()
X_train = tfidf_matrix.toarray()
y_train = [data['label'] for data in train_data]
clf.fit(X_train, y_train)

# 预测测试数据样本的标签
for data in test_data:
    X_test = tfidf_vectorizer.transform([data['text']]).toarray()
    y_pred = clf.predict(X_test)
    data['label'] = y_pred[0]

# 输出测试数据样本的预测结果
for data in test_data:
    print('文本：', data['text'])
    print('标签：', data['label'])