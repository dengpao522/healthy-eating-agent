# 定义逆向最大匹配函数
def backward_maximum_matching(text, dictionary):
    result = []  # 存储切分结果
    max_len = max(len(word) for word in dictionary)
    while len(text) > 0:
        word = None
        for i in range(max_len, 0, -1):  # 从最大长度开始尝试匹配
            if text[-i:] in dictionary:
                word = text[-i:]  # 匹配到了词语
                break
        if word is None:  # 如果没有匹配到词语，则默认切分一个字
            word = text[-1:]
        result.insert(0, word)  # 将切分结果插入列表的开头
        text = text[:-len(word)]  # 更新待切分的文本
    return result

# 测试
dictionary = ['北京市', '北京市民', '民办高中', '天安门广场', '高中']
text = '北京市民办高中'
result = backward_maximum_matching(text, dictionary)
print(result)