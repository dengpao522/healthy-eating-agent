import jieba
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# 准备数据：定义待处理的句子列表
sentences = [
    '这是一个示例句子',
    '这个句子也是用来演示的',
    '可以添加更多的句子作为训练数据'
]

# 分词：使用jieba进行中文分词，得到分词后的句子列表
tokenized_sentences = [jieba.lcut(sentence) for sentence in sentences]

# 创建标记文档：为每个分词后的句子分配一个唯一的标签，并创建TaggedDocument对象
tagged_data = [
    TaggedDocument(words=words, tags=[str(idx)])
    for idx, words in enumerate(tokenized_sentences)
]

# 定义Doc2Vec模型
model = Doc2Vec(vector_size=100,  # 向量维度
                window=5,        # 窗口大小
                min_count=1,     # 最小词频
                dm=0)            # 使用DBoW模型

# 建立模型词汇表
model.build_vocab(tagged_data)

# 训练模型：传入标记文档，指定迭代次数
model.train(tagged_data, total_examples=model.corpus_count, epochs=10)

# 获取文档向量：对新的句子进行分词并将其转换为向量表示
new_sentence = '这是一个要进行推断的句子'
new_tokenized_sentence = jieba.lcut(new_sentence)
doc_vector = model.infer_vector(new_tokenized_sentence)

# 输出结果
print("推断句子的向量表示：", doc_vector)