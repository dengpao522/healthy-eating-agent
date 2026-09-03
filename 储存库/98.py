import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from torch.nn.utils.rnn import pad_sequence
import jieba
from collections import Counter
import pandas as pd
from sklearn.metrics import classification_report

# 加载数据集
file_path = '../data/sentiment.csv'
df = pd.read_csv(file_path, names=['Text', 'Sentiment'], header=0)

# 将情感标签转换为数字：积极为1、消极为0
df['Sentiment'] = df['Sentiment'].apply(lambda x: 1 if x == '正面' else 0)

# 分词和词汇表创建
words = [jieba.lcut(text) for text in df['Text']]
vocab = Counter(word for sublist in words for word in sublist)
vocab = {word: i + 1 for i, word in enumerate(vocab)}  # 词到索引的映射（0为填充位）

# 定义数据集类
class TextDataset(Dataset):
    def __init__(self, texts, labels):
        # 文本转词索引张量并统一长度
        self.texts = [torch.tensor([vocab.get(word, 0) for word in jieba.lcut(text)]) for text in texts]
        self.texts = pad_sequence(self.texts, batch_first=True, padding_value=0)
        self.labels = torch.tensor(labels, dtype=torch.float32)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.texts[idx], self.labels[idx]

# 实例化数据集
texts = df['Text'].tolist()
labels = df['Sentiment'].tolist()
dataset = TextDataset(texts, labels)

# 划分训练集和测试集
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

# 实例化数据加载器
train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=2)

# 模型定义（LSTM情感分类模型）
class SentimentModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super(SentimentModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)  # 词嵌入层
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)  # LSTM层
        self.fc = nn.Linear(hidden_dim, 1)  # 全连接层

    def forward(self, x):
        x = self.embedding(x)
        _, (hidden, _) = self.lstm(x)
        out = self.fc(hidden.squeeze(0))
        return torch.sigmoid(out)  # Sigmoid输出0~1的概率

# 实例化模型、损失函数和优化器
model = SentimentModel(len(vocab) + 1, 50, 100)
criterion = nn.BCELoss()  # 二分类交叉熵损失
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练循环
for epoch in range(10):
    model.train()
    for text, label in train_loader:
        output = model(text)
        loss = criterion(output, label.unsqueeze(1))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f'训练周期 {epoch + 1}，损失：{loss.item()}')

# 模型评估
model.eval()
all_preds = []
all_labels = []
with torch.no_grad():
    for text, label in test_loader:
        output = model(text)
        preds = (output.squeeze() > 0.5).float()
        all_preds.extend(preds.tolist())
        all_labels.extend(label.tolist())

# 输出分类报告
print(classification_report(all_labels, all_preds, target_names=['消极', '积极']))

# 模型预测新文本
test_texts = ['这家餐厅的环境好', '这个服务员态度极不好']
test_data = [torch.tensor([vocab.get(word, 0) for word in jieba.lcut(text)]) for text in test_texts]
test_data = pad_sequence(test_data, batch_first=True, padding_value=0)

with torch.no_grad():
    for text, raw_text in zip(test_data, test_texts):
        output = model(text.unsqueeze(0))
        sentiment = '正面' if output.item() > 0.5 else '负面'
        print(f'文本："{raw_text}" 的情感预测为：{sentiment}')