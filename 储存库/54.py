import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 示例数据和标签
sentences = ["我爱 北京 天安门", "天安门 上 太阳 升"]
tags = [["O", "O", "B-LOC", "I-LOC"], ["B-LOC", "I-LOC", "O", "O"]]

# 将句子和标签组合成数据对，便于后续处理
data = [(sentence.split(), tag) for sentence, tag in zip(sentences, tags)]

# 构建词汇表，包括特殊符号:<PAD>和<UNK>
word_to_ix = {"<PAD>": 0, "<UNK>": 1}
for sentence in sentences:
    for word in sentence.split():
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)

# 构建标签集
tag_to_ix = {"O": 0, "B-LOC": 1, "I-LOC": 2}

# 定义模型
class LSTMTagger(nn.Module):
    def __init__(self, embedding_dim, hidden_dim, vocab_size, tagset_size):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim
        # 词嵌入层
        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)
        # LSTM层，batch_first=True表示输入和输出的第一维是批次大小
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        # 线性层，将LSTM的输出映射到标签空间
        self.hidden2tag = nn.Linear(hidden_dim, tagset_size)

    def forward(self, sentence):
        # 从词嵌入层得到嵌入向量
        embeds = self.word_embeddings(sentence)
        # 通过LSTM层处理嵌入向量
        lstm_out, _ = self.lstm(embeds)
        # 将LSTM层的输出使用线性层转化为标签空间
        tag_space = self.hidden2tag(lstm_out)
        # 计算log_softmax概率得分
        tag_scores = torch.log_softmax(tag_space, dim=-1)
        return tag_scores

# 初始化模型参数
EMBEDDING_DIM = 64
HIDDEN_DIM = 64
model = LSTMTagger(EMBEDDING_DIM, HIDDEN_DIM, len(word_to_ix), len(tag_to_ix))

# 定义损失函数和优化器
loss_function = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

# 训练模型
for epoch in range(300):  # 更多的迭代次数可能会提高模型性能
    for sentence, tag in data:
        # 清除梯度
        model.zero_grad()
        # 准备输入和目标输出
        sentence_in = torch.tensor([[word_to_ix[word] for word in sentence]], dtype=torch.long)
        targets = torch.tensor([[tag_to_ix[t] for t in tag]], dtype=torch.long)
        # 前向传播
        tag_scores = model(sentence_in)
        # 计算损失
        loss = loss_function(tag_scores.view(-1, len(tag_to_ix)), targets.view(-1))
        # 反向传播和优化
        loss.backward()
        optimizer.step()

# 模型预测
ix_to_tag = {ix: tag for tag, ix in tag_to_ix.items()}
with torch.no_grad():
    sentence_to_predict = sentences[0]  # 选择一个句子进行预测
    inputs = torch.tensor([[word_to_ix[word] for word in sentence_to_predict.split()]], dtype=torch.long)
    tag_scores = model(inputs)
    # 得到最可能的标签索引
    predicted_tags_indices = np.argmax(tag_scores.numpy(), axis=2)[0]
    # 将标签索引转换为标签
    predicted_tags = [ix_to_tag[ix] for ix in predicted_tags_indices]
    print("Predicting tags for:", sentence_to_predict)
    # 输出每个词及其预测标签
    for word, tag in zip(sentence_to_predict.split(), predicted_tags):
        print(f"{word}: {tag}")