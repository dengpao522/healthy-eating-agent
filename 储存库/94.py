import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

class SentimentReasonAnalyzer:
    def __init__(self):
        self.vectorizer = None
        self.classifier = None

    def preprocess_text(self, text):
        # 分词
        words = jieba.lcut(text)
        return " ".join(words)

    def train_model(self, X, y):
        # 初始化向量器
        self.vectorizer = TfidfVectorizer()
        # 特征提取
        X_features = self.vectorizer.fit_transform(X)
        # 初始化分类器
        self.classifier = SVC()
        # 训练模型
        self.classifier.fit(X_features, y)

    def analyze_sentiment_reason(self, text):
        # 预处理文本
        preprocessed_text = self.preprocess_text(text)
        # 提取特征
        features = self.vectorizer.transform([preprocessed_text])
        # 执行文本情感原因分析
        predicted_label = self.classifier.predict(features)[0]
        reasons = {0: "悲伤", 1: "愤怒", 2: "恐惧", 3: "喜悦", 4: "厌恶"}  # 根据实际情况定义情感标签
        return reasons[predicted_label]

# 示例文本和相应的情感标签
texts = [
    "这个电影真的很感人，让我热泪盈眶。",
    "这个产品太差了，完全不值得购买。",
    "这次的旅行真是太好玩了，一切都很完美。",
    "这个新闻让我感到非常愤怒，我们需要采取行动。",
    "我对未来感到恐惧，不知道会发生什么。"
]
labels = [0, 1, 3, 1, 2]

analyzer = SentimentReasonAnalyzer()
analyzer.train_model(texts, labels)

test_text = "这本书真是太催泪了，看得我心情很沉重。"
reason = analyzer.analyze_sentiment_reason(test_text)
print(f"情感原因分析结果：{reason}")