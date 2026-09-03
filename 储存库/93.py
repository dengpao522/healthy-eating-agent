import jieba
import jieba.posseg as pseg
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import numpy as np

# 训练数据样本 - 包含文本、情感目标和情感标签
train_data = [
    ("这部电影太精彩了，我非常喜欢！", "电影", "positive"),
    ("今天天气真好，心情愉快。", "天气", "positive"),
    ("这个产品质量太差，非常失望。", "产品", "negative"),
    ("服务态度很差，不推荐购买。", "服务态度", "negative")
]

# 分词处理
def tokenize(text):
    return list(jieba.cut(text))

# 情感目标识别函数
def identify_sentiment_target(text):
    words = pseg.cut(text)
    potential_targets = []
    # 根据词性识别可能的情感目标（名词和名词短语）
    for word, flag in words:
        if flag.startswith('n'):  # 名词
            potential_targets.append(word)
    return potential_targets

# 特征提取
vectorizer = TfidfVectorizer(tokenizer=tokenize)
X_text = vectorizer.fit_transform([data[0] for data in train_data])

# 提取情感目标特征
X_targets = []
for data in train_data:
    text = data[0]
    known_target = data[1]
    # 将已知目标编码为特征
    targets = identify_sentiment_target(text)
    if known_target in targets:
        target_idx = targets.index(known_target)
    else:
        target_idx = -1
    X_targets.append([target_idx])

# 合并特征
X_combined = np.hstack((X_text.toarray(), X_targets))

# 提取情感标签
y_train = [data[2] for data in train_data]

# 模型训练
sentiment_model = SVC()
sentiment_model.fit(X_combined, y_train)

# 测试数据
test_text = "这是一部很棒的电影！"
test_targets = identify_sentiment_target(test_text)
print("识别到的可能情感目标:", test_targets)

if test_targets:
    # 提取文本特征
    X_test_text = vectorizer.transform([test_text]).toarray()
    # 假设第一个识别到的目标是正确的
    target_idx = 0
    X_test_combined = np.hstack((X_test_text, [[target_idx]]))
    # 情感目标及情感极性预测
    predicted_sentiment = sentiment_model.predict(X_test_combined)[0]
    print("预测结果:", test_targets[target_idx], predicted_sentiment)
else:
    print("未识别到情感目标")