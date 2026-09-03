import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import warnings

warnings.filterwarnings("ignore")

# 加载数据集
file_path = '../data/sentiment.csv'
df = pd.read_csv(file_path)

# 定义停用词列表
stop_words = ['的', '了', '这个', '非常', '一次', '很']
corpus_X = []
corpus_y = []

# 分词和特征提取
for _, row in df.iterrows():
    text = row['Text']
    label = row['Sentiment']
    seg_list = jieba.cut(text)
    seg_list = [word for word in seg_list if word not in stop_words]
    corpus_X.append(' '.join(seg_list))
    corpus_y.append(label)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus_X)
y = corpus_y

# 数据集划分
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 朴素贝叶斯分类器
nb_classifier = MultinomialNB()
nb_classifier.fit(X_train, y_train)
nb_pred = nb_classifier.predict(X_test)
print('朴素贝叶斯分类器结果：')
print(classification_report(y_test, nb_pred))

# SVM分类器
svm_classifier = SVC(kernel='linear')
svm_classifier.fit(X_train, y_train)
svm_pred = svm_classifier.predict(X_test)
print('支持向量机分类器结果：')
print(classification_report(y_test, svm_pred))

# 决策树分类器
dt_classifier = DecisionTreeClassifier()
dt_classifier.fit(X_train, y_train)
dt_pred = dt_classifier.predict(X_test)
print('决策树分类器结果：')
print(classification_report(y_test, dt_pred))

# 随机森林分类器
rf_classifier = RandomForestClassifier()
rf_classifier.fit(X_train, y_train)
rf_pred = rf_classifier.predict(X_test)
print('随机森林分类器结果：')
print(classification_report(y_test, rf_pred))

# 使用5折交叉验证评估模型性能
models = {
    '朴素贝叶斯': MultinomialNB(),
    '支持向量机': SVC(kernel='linear'),
    '决策树': DecisionTreeClassifier(),
    '随机森林': RandomForestClassifier()
}

for model_name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5)
    print(f'{model_name}交叉验证平均准确率：{scores.mean():.2f}')