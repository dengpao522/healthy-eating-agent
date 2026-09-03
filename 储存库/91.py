import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm

# 训练数据样本
train_data = [
    ("这部电影太棒了，我非常喜欢!", "积极"),
    ("这家餐厅的菜很难吃，服务态度也很差。", "消极"),
    ("今天的天气非常好，心情很愉快。", "积极"),
    ("这本书写得真好，深入浅出，推荐给大家。", "积极"),
    ("这个手机真是垃圾，根本用不了多久就坏了。", "消极"),
    ("这个游戏太无聊了，玩一会就腻了。", "消极"),
    ("这部电影太无聊了，看一会就睡了。", "消极"),
    ("这首歌曲很动听，让人心情愉悦。", "积极")
]

# 定义分词和去除停用词函数
def tokenize(text):
    seg_list = jieba.cut(text)
    return " ".join(seg_list)

stop_words = ["这", "的", "了", "非常"]

# 对训练数据样本进行分词和去除停用词处理
processed_train_data = [(tokenize(text), label) for text, label in train_data]

# 特征提取
vectorizer = TfidfVectorizer(stop_words=stop_words)
X_train = vectorizer.fit_transform([data[0] for data in processed_train_data])
y_train = [data[1] for data in processed_train_data]

# 模型训练
classifier = svm.SVC()
classifier.fit(X_train, y_train)

# 分类新文本
new_text = "这个电影太差了，一点都不好看。"
processed_new_text = tokenize(new_text)
X_new = vectorizer.transform([processed_new_text])
prediction = classifier.predict(X_new)[0]

# 输出分类结果
print("文本：", new_text)
print("情感分类：", prediction)