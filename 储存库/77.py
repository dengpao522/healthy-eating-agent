import jieba
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# 准备数据：定义待处理的句子列表
sentences = [
    '中文NLP',
    'DM模型用于文本表示和语义建模',
    '文本分类任务需要将句子转换为向量表示'
]

# 分词：使用jieba进行中文分词
tokenized_sentences = [jieba.lcut(sentence) for sentence in sentences]

# 构建标记文档列表：为每个分词后的句子分配一个唯一的标签
tagged_documents = [
    TaggedDocument(words=words, tags=[str(i)])
    for i, words in enumerate(tokenized_sentences)
]

# 定义DM模型
# vector_size：向量维度
# window：窗口大小
# min_count：最小词频
# dm：模型选择（1表示使用DM模型，0表示使用DBoW模型）
model = Doc2Vec(vector_size=100, window=5, min_count=1, dm=1)

# 建立模型词汇表
model.build_vocab(tagged_documents)

# 训练模型
model.train(tagged_documents, total_examples=model.corpus_count, epochs=10)

# 获取句子的向量表示：将分词后的句子转换为向量
sentence_vectors = [model.infer_vector(words) for words in tokenized_sentences]

# 应用模型：将新句子转换为向量
new_sentence = '新的句子'
new_tokenized_sentence = jieba.lcut(new_sentence)
new_sentence_vector = model.infer_vector(new_tokenized_sentence)

# 输出结果
for i, sentence_vector in enumerate(sentence_vectors):
    print(f"句子{i+1}的向量表示：{sentence_vector}")
print(f"新句子的向量表示：{new_sentence_vector}")