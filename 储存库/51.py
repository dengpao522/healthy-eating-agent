import numpy as np

# 定义词性集合，这里的词性包括名词(n)、动词(v)、形容词(a)和副词(d)
pos_set = {'n', 'v', 'a', 'd'}
# 定义初始状态概率分布，即句子首词的词性分布概率
init_prob = {'n': 0.4, 'v': 0.3, 'a': 0.2, 'd': 0.1}
# 定义状态转移概率矩阵，即从一个词性转移到另一个词性的概率
trans_prob = {
    'n': {'n': 0.2, 'v': 0.5, 'a': 0.2, 'd': 0.1},
    'v': {'n': 0.3, 'v': 0.1, 'a': 0.3, 'd': 0.3},
    'a': {'n': 0.3, 'v': 0.4, 'a': 0.1, 'd': 0.2},
    'd': {'n': 0.1, 'v': 0.1, 'a': 0.4, 'd': 0.4}
}
# 定义发射概率矩阵，即给定词性产生特定词的概率
emit_prob = {
    'n': {'我': 0.1, '你': 0.2, '他': 0.3},
    'v': {'吃': 0.4, '喝': 0.3, '走': 0.3},
    'a': {'好': 0.5, '高': 0.4, '快': 0.1},
    'd': {'很': 0.7, '非常': 0.2, '太': 0.1}
}

# 定义观测序列，即输入的句子
obs_sequence = ['我', '很', '好']


# 实现维特比算法，进行词性标注
def viterbi(obs_seq, pos_set, init_prob, trans_prob, emit_prob):
    # 初始化动态规划矩阵，用于保存每个时刻每个词性的最大概率
    dp = np.zeros((len(pos_set), len(obs_seq)))
    # 初始化路径矩阵，用于保存每步的最优路径
    path = np.zeros((len(pos_set), len(obs_seq)), dtype=int)

    # 初始化第一个时刻的词性概率
    pos_list = list(pos_set)
    for i, pos in enumerate(pos_list):
        dp[i][0] = init_prob[pos] * emit_prob[pos].get(obs_seq[0], 0)

    # 迭代计算动态规划矩阵和路径矩阵
    for t in range(1, len(obs_seq)):
        for i, cur_pos in enumerate(pos_list):
            max_prob = -1
            max_path = -1
            for j, prev_pos in enumerate(pos_list):
                prob = dp[j][t - 1] * trans_prob[prev_pos].get(cur_pos, 0) * emit_prob[cur_pos].get(obs_seq[t], 0)
                if prob > max_prob:
                    max_prob = prob
                    max_path = j
            dp[i][t] = max_prob
            path[i][t] = max_path

    # 回溯最优路径
    optimal_path = []
    last_pos = np.argmax(dp[:, -1])
    optimal_path.append(last_pos)
    for t in range(len(obs_seq) - 1, 0, -1):
        last_pos = path[last_pos][t]
        optimal_path.append(last_pos)
    optimal_path.reverse()

    return optimal_path


# 进行词性标注
optimal_path = viterbi(obs_sequence, pos_set, init_prob, trans_prob, emit_prob)

# 输出词性标注结果
pos_list = list(pos_set)
for i, pos_index in enumerate(optimal_path):
    pos = pos_list[pos_index]
    print(f"{obs_sequence[i]}/{pos}")