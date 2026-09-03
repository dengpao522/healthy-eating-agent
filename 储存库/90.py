import nltk.classify as cf
import nltk.classify.util as cu
import jieba


def setiment(sentences):
    # 文本转换为特征并提取特征
    pos_data = []
    with open('../data/pos.txt', 'r+', encoding='utf-8') as pos:  # 读取积极评论数据
        while True:
            words = pos.readline()
            if words:
                positive = {}  # 创建积极评论数据的词典
                words = jieba.cut(words)  # 使用jieba对积极评论数据进行分词
                for word in words:
                    positive[word] = True
                pos_data.append((positive, 'POSITIVE'))  # 对积极词赋予POSITIVE标签
            else:
                break

    neg_data = []
    with open('../data/neg.txt', 'r+', encoding='utf-8') as neg:  # 读取消极评论数据
        while True:
            words = neg.readline()
            if words:
                negative = {}  # 创建消极评论数据的词典
                words = jieba.cut(words)  # 使用jieba对消极评论数据进行分词
                for word in words:
                    negative[word] = True
                neg_data.append((negative, 'NEGATIVE'))  # 对消极词赋予NEGATIVE标签
            else:
                break

    # 划分训练集与测试集
    pos_num, neg_num = int(len(pos_data) * 0.8), int(len(neg_data) * 0.8)
    train_data = pos_data[:pos_num] + neg_data[:neg_num]  # 划分80%的数据作为训练集
    test_data = pos_data[pos_num:] + neg_data[neg_num:]  # 剩余的20%的数据作为测试集

    # 构建朴素贝叶斯分类器
    model = cf.NaiveBayesClassifier.train(train_data)
    ac = cu.accuracy(model, test_data)
    print('准确率为：' + str(ac))

    tops = model.most_informative_features()
    # 输出信息量较大的前10个特征
    print('\n信息量较大的前10个特征：')
    for top in tops[:10]:
        print(top[0])

    for sentence in sentences:
        feature = {}
        words = jieba.cut(sentence)
        for word in words:
            feature[word] = True
        pcls = model.prob_classify(feature)
        sent = pcls.max()  # 情感标签（POSITIVE或NEGATIVE）
        prob = pcls.prob(sent)  # 概率
        print(f'\n“{sentence}”的情感标签为{sent}，概率为{round(prob * 100, 2)}%')


if __name__ == '__main__':
    # 新的评论数据
    sentences = [
        '破烂',
        '手感不错，推荐购买',
        '刚开始吧还不错，但是后面越来越卡，差评',
        '哈哈哈哈，我很喜欢',
        '今天很开心'
    ]
    setiment(sentences)