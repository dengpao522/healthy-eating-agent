import requests
from bs4 import BeautifulSoup
from openccc import OpenCC

# 定义繁体中文转换为简体中文的函数
def traditional_to_simplified(text):
    cc = OpenCC('t2s')  # 繁体中文转换为简体中文
    return cc.convert(text)

# 获取网页内容
url = "https://***"  # 《西游记》对应网址
response = requests.get(url)
response.encoding = 'utf-8'  # 确保正确的编码

# 解析网页内容
soup = BeautifulSoup(response.text, 'html.parser')

# 假设需要获取<body>标签内的所有文本
body_text = soup.body.get_text()

# 将繁体中文转换为简体中文
simplified_text = traditional_to_simplified(body_text)

# 将文本分割为行并取100～104行查看
lines = simplified_text.splitlines()
selected_lines = lines[100:105]  # Python 列表切片不包括结束索引

# 输出选定的行
for line in selected_lines:
    print(line)


import requests
from bs4 import BeautifulSoup
from opencc import OpenCC  # 修正包名：opencc 而非 openccc

# 定义繁体转简体函数
def traditional_to_simplified(text):
    cc = OpenCC('t2s')  # t2s：繁体转简体
    return cc.convert(text)

# 替换为《西游记》繁体原文公开URL（示例）
url = "https://zh.wikisource.org/zh-tw/%E8%A5%BF%E6%B8%B8%E8%AE%B0"
# 添加请求头，避免被反爬
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
}

# 获取网页内容（添加异常处理）
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    response.raise_for_status()  # 捕获HTTP错误
except requests.exceptions.RequestException as e:
    print(f"网页请求失败：{e}")
    exit()

# 解析网页，提取正文（过滤无关标签）
soup = BeautifulSoup(response.text, 'html.parser')
# 仅提取<p>标签内的文本（聚焦正文）
p_tags = soup.find_all('p')
body_text = '\n'.join([p.get_text().strip() for p in p_tags if p.get_text().strip()])

# 繁体转简体
simplified_text = traditional_to_simplified(body_text)

# 取前5行（原100-105行无内容，适配测试URL）
lines = simplified_text.splitlines()
selected_lines = lines[:5] if len(lines)>=5 else lines

# 输出结果
print("《西游记》简体文本（前5行）：")
for idx, line in enumerate(selected_lines, 1):
    print(f"{idx}. {line}")


import pandas as pd
import re

def preprocess_text(text):
    # 清洗评论文本：去除标点、数字、多余空格
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def build_corpus(input_file, output_file):
    # 从CSV读取数据
    df = pd.read_csv(input_file)
    # 提取评论并去除空值
    comments = df['comment'].dropna().tolist() if 'comment' in df.columns else []
    # 预处理评论
    preprocessed_comments = [preprocess_text(comment) for comment in comments]
    # 写入文本文件（每个评论一行）
    with open(output_file, 'w', encoding='utf-8') as f:
        for comment in preprocessed_comments:
            if comment:  # 跳过空评论
                f.write(comment + '\n')

# 路径配置
input_file = '../data/ratings.csv'
output_file = '../data/movie_comments.txt'
build_corpus(input_file, output_file)
print("电影评论语料库已建立")


# 随机查看一条评论
import random
def get_random_comment(corpus_file):
    with open(corpus_file, 'r', encoding='utf-8') as f:
        comments = f.readlines()
    random_comment = random.choice(comments)
    return random_comment.strip()

corpus_file = '../data/movie_comments.txt'
random_comment = get_random_comment(corpus_file)
print("随机选择的评论: ", random_comment)


import jieba
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# 1. 读取文本文件
with open("../data/党的二十大报告.txt", "r", encoding="gbk") as f:
    text = f.read()

# 2. 读取中文停用词表
with open("../data/中文停用词表.txt", "r", encoding="gbk") as f:
    stopwords = f.read()

# 3. 分词处理
seg_list = jieba.cut(text)
words = " ".join(seg_list)

# 4. 过滤停用词
def remove_stopwords(text, stopwords):
    text_without_stopwords = [word for word in re.split(r'\W+', text) if word not in stopwords]
    return ' '.join(text_without_stopwords)
text_without_stopwords = remove_stopwords(words, stopwords)

# 5. 统计词频
word_count = Counter(text_without_stopwords.split())

# 6. 输出前10高频词
n = 10
top_words = word_count.most_common(n)
for word, count in top_words:
    print(f"词语: {word} 频次: {count}")

# 7. 生成并显示词云
wordcloud = WordCloud(
    background_color='white',
    font_path=r'C:\Windows\Fonts\simsun',  # 指定中文字体路径
    scale=2,
    stopwords=stopwords
).generate_from_frequencies(word_count)

plt.figure(dpi=600)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')  # 隐藏坐标轴
plt.show()