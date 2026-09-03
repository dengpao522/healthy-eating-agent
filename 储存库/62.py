import jieba.posseg as pseg
import networkx as nx


def textrank_keyword(text, topK=10):
    """
    使用TextRank算法提取关键词
    参数如下
    text: 待处理的文本
    topK: 返回的关键词数量，默认为10
    返回值如下
    关键词列表，按重要性排序
    """
    # 使用jieba进行中文分词和词性标注，只保留名词
    words = pseg.cut(text)
    word_list = [word for word, flag in words if flag.startswith('n')]

    # 构建图结构
    graph = nx.Graph()
    graph.add_nodes_from(set(word_list))

    # 计算词之间的相关度
    for i, word in enumerate(word_list):
        for j in range(i + 1, len(word_list)):
            word_i = word_list[i]
            word_j = word_list[j]
            if graph.has_edge(word_i, word_j):
                graph[word_i][word_j]['weight'] += 1
            else:
                graph.add_edge(word_i, word_j, weight=1)

    # 使用PageRank算法计算节点的重要性
    pagerank = nx.pagerank(graph)

    # 根据节点重要性进行关键词提取
    keywords = sorted(pagerank, key=pagerank.get, reverse=True)[:topK]
    return keywords


# 使用示例
text = "这是一个使用TextRank算法实现关键词提取的示例。"
keywords = textrank_keyword(text)
for keyword in keywords:
    print(keyword)