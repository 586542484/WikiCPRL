# -*- coding: utf-8 -*-
import pandas as pd
import random

d = pd.read_csv('cs_preqs.csv', header=None)
A_concepts = d[0].tolist()
B_concepts = d[1].tolist()
# print(A_concepts)

con_list = list(dict.fromkeys(A_concepts + B_concepts))  # 概念去重(保留顺序)
# print(len(con_list))
# print(con_list)
# df = pd.DataFrame(con_list)
# df.to_csv('data/concepts.csv', index=None, header=None)

# 随机生成和正例数量相同的负例
preqs_list = d.values
# 为 preqs_list 添加标注列
preqs_list = [(pair[0], pair[1], 1) for pair in preqs_list]
# preqs概念对的数量
num_pairs = len(preqs_list)
print(num_pairs)
# 初始化空列表用于存储随机概念对
random_pairs = []
# 生成随机概念对
while len(random_pairs) < num_pairs:
    # 随机选择两个不同的概念
    random_concepts = random.sample(con_list, 2)

    # 组合成新的概念对
    new_pair = tuple(random_concepts)

    # 检查是否与原始概念对有重复
    if new_pair not in preqs_list and new_pair not in random_pairs:
        random_pairs.append(new_pair)

# 为 random_pairs 添加标注列
random_pairs = [(pair[0], pair[1], 0) for pair in random_pairs]

all_pairs = preqs_list + random_pairs
random.shuffle(all_pairs)

# 转为 DataFrame
df = pd.DataFrame(all_pairs, columns=['A', 'B', 'result'])

# 存储到 CSV 文件
df.to_csv('cs_concept_pairs.csv', index=False, float_format='%.0f')
