import sklearn_crfsuite
from sklearn_crfsuite import metrics
import joblib
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.preprocessing import MultiLabelBinarizer


# 定义CorpusProcess类来处理语料库
class CorpusProcess(object):
    def __init__(self):
        # 定义文件读取路径和读取方式
        self.train_corpus_path = "../data/food.txt"
        self._maps = {'n': 'NOUN', 'ns': 'LOC'}

    # 读取语料
    def read_corpus_from_file(self, file_path):
        f = open(file_path, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        return lines

    # 由词性提取标签
    def pos_to_tag(self, p):
        t = self._maps.get(p, None)  # 根据词性映射表提取对应的标签
        return t if t else 'O'

    # 标签使用BIO模式
    def tag_perform(self, tag, index):
        if index == 0 and tag != 'O':  # 如果是第一个词，且未被标记为O，则标记为B
            return 'B_{}'.format(tag)
        elif tag != 'O':  # 如果是其他词，且未被标记为O，则标记为I
            return 'I_{}'.format(tag)
        else:
            return tag

    # 初始化
    def initialize(self):
        lines = self.read_corpus_from_file(self.train_corpus_path)
        words_list = [line.strip().split(' ') for line in lines if line.strip()]
        del lines
        self.init_sequence(words_list)

    # 初始化序列
    def init_sequence(self, words_list):
        # 初始化词序列、词性序列、标签序列
        words_seq = [[word.split('/')[0] for word in words] for words in words_list]
        pos_seq = [[word.split('/')[1] for word in words] for words in words_list]
        tag_seq = [[self.pos_to_tag(p) for p in pos] for pos in pos_seq]

        # 处理词性序列
        self.pos_seq = [[[pos_seq[index][i] for _ in range(len(words_seq[index][i]))]
                         for i in range(len(pos_seq[index]))] for index in range(len(pos_seq))]

        # 处理标签序列（BIO模式）
        self.tag_seq = [[[self.tag_perform(tag_seq[index][i], w) for w in range(len(words_seq[index][i]))]
                         for i in range(len(tag_seq[index]))] for index in range(len(tag_seq))]

        # 词性序列前后添加占位符
        self.pos_seq = [['un'] + [self.pos_to_tag(p) for pos in pos_seq for p in pos] + ['un']
                        for pos_seq in self.pos_seq]

        # 标签序列扁平化
        self.tag_seq = [[t for tag in tag_seq for t in tag] for tag_seq in self.tag_seq]

        # 词序列前后添加BOS/EOS标记
        self.word_seq = [['<BOS>'] + [w for word in word_seq for w in word] + ['<EOS>']
                         for word_seq in words_seq]