dictionary = ['北京市', '北京市民', '民办高中', '天安门广场', '高中']
text = '北京市民办高中'

def forward_maximum_matching(text, dictionary):
    word_segmentation = []  # 用于存储分词结果
    text_length = len(text)  # 待分词文本长度
    while text_length > 0:
        # 限制匹配词语的最大长度为词典最长词语的长度、剩余文本长度中较小的值
        max_word_length = min(text_length, len(max(dictionary, key=lambda x: len(x))))
        # 正向最大匹配
        forward_word = text[:max_word_length]  # 从文本开头位置截取最大长度的文本
        while forward_word not in dictionary:  # 若当前截取的文本不在词典中
            # 若截取文本长度为1，则无法再进行切分，将其作为一个独立词语
            if len(forward_word) == 1:
                break
            forward_word = forward_word[:-1]  # 若不是独立词语，则减少截取文本长度
        word_segmentation.append(forward_word)  # 将匹配到的词语添加到分词结果
        text = text[len(forward_word):]  # 更新待分词文本（去除已匹配的部分）
        text_length = len(text)  # 更新待分词文本长度
    return word_segmentation

# 测试
seg_result = forward_maximum_matching(text, dictionary)
print(seg_result)