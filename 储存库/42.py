import numpy as np

def viterbi(text, states, start_prob, trans_prob, emit_prob):
    # 初始化
    V = [{}]
    path = {}
    # 初始时刻
    for state in states:
        V[0][state] = start_prob[state] * emit_prob[state][text[0]]
        path[state] = [state]
    # 动态规划
    for t in range(1, len(text)):
        V.append({})
        new_path = {}
        for state in states:
            # 计算当前状态的最大概率及对应的前序状态
            prob, prev_state = max(
                [
                    (V[t-1][prev_state] * trans_prob[prev_state][state] * emit_prob[state][text[t]], prev_state)
                    for prev_state in states
                ]
            )
            V[t][state] = prob
            new_path[state] = path[prev_state] + [state]
        path = new_path
    # 终止时刻，选择最终状态的最大概率路径
    prob, state = max((V[len(text)-1][state], state) for state in states)
    seg_list = path[state]
    return seg_list

# 定义HMM参数
states = ['B', 'M', 'E', 'S']  # B:词首, M:词中, E:词尾, S:单字成词
start_prob = {'B': 0.5, 'M': 0, 'E': 0, 'S': 0.5}
trans_prob = {
    'B': {'B': 0.2, 'M': 0.7, 'S': 0.1, 'E': 0},
    'M': {'B': 0, 'M': 0.1, 'S': 0.8, 'E': 0.1},
    'E': {'B': 0.2, 'M': 0.3, 'S': 0.4, 'E': 0.1},
    'S': {'B': 0.3, 'M': 0.5, 'S': 0, 'E': 0.2}
}
emit_prob = {
    'B': {'我': 0.1, '爱': 0, '中': 0, '国': 0, '人': 0},
    'M': {'我': 0, '爱': 0.1, '中': 0, '国': 0, '人': 0},
    'E': {'我': 0, '爱': 0, '中': 0.1, '国': 0, '人': 0},
    'S': {'我': 0, '爱': 0.4, '中': 0, '国': 0.1, '人': 0}
}

# 分词
text = '我爱中国人'
seg_list = viterbi(text, states, start_prob, trans_prob, emit_prob)

# 输出分词结果
for i in range(len(seg_list)):
    if seg_list[i] == 'B' or seg_list[i] == 'S':
        print(text[i], end=' ')
    else:
        print(text[i], end='')