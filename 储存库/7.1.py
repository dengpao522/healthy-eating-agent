import jieba

# 1. 准备数据
sentences = ['我喜欢吃苹果。', '他喜欢吃香蕉。', '我喜欢吃橙子。']

# 2. 分词（核心改进：jieba失败时自动用字符分割兜底）
tokenized_sentences = []
for sentence in sentences:
    if sentence.strip():
        # 尝试jieba分词
        try:
            words = jieba.lcut(sentence)
            # 若jieba返回空，改用字符分割（过滤标点）
            if not words or words is None:
                print(f"jieba分词为空，自动切换字符分割：{sentence}")
                words = [c for c in sentence if c not in '。，！？']
        except Exception as e:
            # 任何jieba异常都切换字符分割
            print(f"jieba分词出错：{e}，自动切换字符分割：{sentence}")
            words = [c for c in sentence if c not in '。，！？']
        # 确保最终有分词结果
        if words:
            tokenized_sentences.append(words)
        else:
            print(f"警告：句子「{sentence}」无有效分词结果")
    else:
        print(f"警告：句子「{sentence}」是空字符串")

# 3. 构建词汇表（移除强制报错，改为友好提示+退出）
word_set = set()
if not tokenized_sentences:
    print("错误：所有句子均无有效分词结果，程序退出")
    exit(1)  # 友好退出，而非抛出异常

for words in tokenized_sentences:
    if isinstance(words, (list, tuple)):
        word_set.update(words)
    else:
        print(f"警告：非可迭代的分词结果 {words}，已跳过")

vocab = sorted(list(word_set))  # 排序保证结果稳定

# 4. 生成独热向量（字典映射优化）
word2idx = {word: idx for idx, word in enumerate(vocab)}

def one_hot_vectorize(sentence_words, word2idx):
    vector = [0] * len(word2idx)
    for word in sentence_words:
        if word in word2idx:
            vector[word2idx[word]] = 1
    return vector

# 5. 文本向量化
vectors = [one_hot_vectorize(sent, word2idx) for sent in tokenized_sentences]

# 6. 输出结果（适配分词后的数据长度）
print("\n===== 最终结果 =====")
print("词汇表:", vocab)
print("\n文本向量:")
for i in range(len(tokenized_sentences)):
    # 避免zip长度不匹配问题
    orig_sent = sentences[i] if i < len(sentences) else "未知句子"
    print(f"句子{i+1}: {orig_sent}")
    print(f"向量: {vectors[i]}")
    print()