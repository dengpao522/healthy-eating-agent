import jieba

# 准备数据
sentences = ['我喜欢吃苹果。', '他喜欢吃香蕉。', '我喜欢吃橙子。']

# 分词
tokenized_sentences = [jieba.lcut(sentence) for sentence in sentences]

# 构建词汇表
word_set = set()
for words in tokenized_sentences:
    word_set.update(words)
vocab = list(word_set)

# 生成独热向量
def one_hot_vectorize(sentence, vocab):
    vector = [0] * len(vocab)
    for word in sentence:
        if word in vocab:
            index = vocab.index(word)
            vector[index] = 1
    return vector

# 文本向量化
vectors = [one_hot_vectorize(sentence, vocab) for sentence in tokenized_sentences]

# 输出词汇表和文本向量
print("词汇表: ", vocab)
print("文本向量: ")
for i, sentence in enumerate(sentences):
    print(f"句子{i+1}: {sentence}")
    print(vectors[i])
    print()
