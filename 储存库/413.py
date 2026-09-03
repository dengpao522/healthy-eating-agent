# 需先定义forward_maximum_matching和backward_maximum_matching函数
def forward_maximum_matching(text, dictionary):
    word_segmentation = []
    text_length = len(text)
    max_word_len = max(len(word) for word in dictionary)
    while text_length > 0:
        max_len = min(text_length, max_word_len)
        forward_word = text[:max_len]
        while forward_word not in dictionary:
            if len(forward_word) == 1:
                break
            forward_word = forward_word[:-1]
        word_segmentation.append(forward_word)
        text = text[len(forward_word):]
        text_length = len(text)
    return word_segmentation


def backward_maximum_matching(text, dictionary):
    result = []
    max_len = max(len(word) for word in dictionary)
    while len(text) > 0:
        word = None
        for i in range(max_len, 0, -1):
            if text[-i:] in dictionary:
                word = text[-i:]
                break
        if word is None:
            word = text[-1:]
        result.insert(0, word)
        text = text[:-len(word)]
    return result


# 定义双向最大匹配函数
def bidirectional_maximum_matching(text, dictionary):
    # 获取正向最大匹配结果
    forward_result = forward_maximum_matching(text, dictionary)
    # 获取逆向最大匹配结果
    backward_result = backward_maximum_matching(text, dictionary)

    # 优先选择分词数量更少的结果
    if len(forward_result) < len(backward_result):
        return forward_result
    elif len(forward_result) > len(backward_result):
        return backward_result
    else:
        # 若分词数量相同，选择单字词较少的结果
        forward_single = sum(1 for word in forward_result if len(word) == 1)
        backward_single = sum(1 for word in backward_result if len(word) == 1)
        if forward_single < backward_single:
            return forward_result
        else:
            return backward_result


# 测试
dictionary = ['北京市', '北京市民', '民办高中', '天安门广场', '高中']
text = '北京市民办高中'
bidirectional_result = bidirectional_maximum_matching(text, dictionary)
print(bidirectional_result)