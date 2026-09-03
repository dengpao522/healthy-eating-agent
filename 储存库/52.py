import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

# 定义基于LSTM的词性标注模型
class POSModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(POSModel, self).__init__()
        # 初始化隐藏层大小
        self.hidden_size = hidden_size
        # 定义词嵌入层，将每个词转化为固定大小的向量
        self.embedding = nn.Embedding(input_size, hidden_size)
        # 定义LSTM层，用于处理序列数据
        self.lstm = nn.LSTM(hidden_size, hidden_size)
        # 定义线性层，从隐藏状态映射到标签空间
        self.hidden2tag = nn.Linear(hidden_size, output_size)

    def forward(self, sentence):
        # 通过词嵌入层将输入句子中的词转换为向量
        embeds = self.embedding(sentence)
        # LSTM层处理嵌入向量，输出序列中每个词的隐藏状态
        lstm_out, _ = self.lstm(embeds.view(len(sentence), 1, -1))
        # 将LSTM层的输出使用线性层转换为标签空间
        tag_space = self.hidden2tag(lstm_out.view(len(sentence), -1))
        # 计算标签的Log-softmax，作为最终的输出概率
        tag_scores = F.log_softmax(tag_space, dim=1)
        return tag_scores

# 准备训练数据集和测试数据集
train_data = [
    (['我', '是', '一个', '学生'], ['pronoun', 'verb', 'determiner', 'noun']),
    (['今天', '天气', '非常', '好'], ['noun', 'noun', 'adverb', 'adjective']),
    (['我们', '正在', '学习', '编程'], ['pronoun', 'adverb', 'verb', 'noun']),
    (['他', '每天', '跑步', '一小时'], ['pronoun', 'adverb', 'verb', 'noun']),
    (['这本', '书', '很', '有趣'], ['determiner', 'noun', 'adverb', 'adjective']),
    (['老师', '讲解', '得', '很', '清楚'], ['noun', 'verb', 'adverb', 'adverb', 'adjective']),
    (['市中心', '有', '很多', '高楼'], ['noun', 'verb', 'adjective', 'noun']),
    (['她', '喜欢', '吃', '辣的'], ['pronoun', 'verb', 'verb', 'adjective']),
    (['这件', '事情', '让', '人', '困惑'], ['determiner', 'noun', 'verb', 'noun', 'adjective']),
    (['请', '静静地', '听我', '讲'], ['verb', 'adverb', 'verb', 'verb']),
    (['图书馆', '里', '非常', '安静'], ['noun', 'adverb', 'adverb', 'adjective'])
]

test_data = [
    (['明天', '你', '准备', '干什么'], ['noun', 'pronoun', 'verb', 'verb']),
    (['这个', '手机', '多少', '钱'], ['determiner', 'noun', 'adverb', 'noun'])
]

# 构建词汇表，将文本转换为数字索引以进行处理
word_to_ix = {}
for sentence, tags in train_data + test_data:
    for word in sentence:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)

# 词性标签到数字索引的映射
tag_to_ix = {'pronoun': 0, 'verb': 1, 'determiner': 2, 'noun': 3, 'adverb': 4, 'adjective': 5}

# 定义模型的超参数
EMBEDDING_DIM = 100
HIDDEN_DIM = 100
OUTPUT_DIM = len(tag_to_ix)

# 初始化词性标注模型
model = POSModel(len(word_to_ix), EMBEDDING_DIM, HIDDEN_DIM)
# 使用负对数似然损失和随机梯度下降优化器
loss_function = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

# 训练模型
for epoch in range(100):
    for sentence, tags in train_data:
        # 清除模型先前的梯度
        model.zero_grad()
        # 准备模型输入和目标标签
        sentence_in = torch.tensor([word_to_ix[word] for word in sentence], dtype=torch.long)
        targets = torch.tensor([tag_to_ix[tag] for tag in tags], dtype=torch.long)
        # 前向传播
        tag_scores = model(sentence_in)
        # 计算损失
        loss = loss_function(tag_scores, targets)
        # 反向传播和优化
        loss.backward()
        optimizer.step()

# 测试模型性能
with torch.no_grad():
    for sentence, tags in test_data:
        sentence_in = torch.tensor([word_to_ix[word] for word in sentence], dtype=torch.long)
        scores = model(sentence_in)
        _, predicted_tags = torch.max(scores, 1)
        predicted_tags = [list(tag_to_ix.keys())[list(tag_to_ix.values()).index(tag)] for tag in predicted_tags]
        print('输入句子：', sentence)
        print('预测词性：', predicted_tags)