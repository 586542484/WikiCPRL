import math
import json

import pandas as pd
import numpy as np


# 读取包含概念backlinks的JSON文件
with open('backlinks_dict.json', 'r', encoding='utf-8') as file:
    backlinks_dict = json.load(file)

# 读取包含概念对的CSV文件
df_concepts = pd.read_csv(r'D:\Code\PycharmProjects\LK_project\MHAVGAE-main\2023-10-15\University course\data\cs_concept_pairs.csv')

# 英文维基百科词条总数：6,641,740
PMI_count = []
count = 0

# 计算每行中概念A和概念B的backlinks的差异
for index, row in df_concepts.iterrows():
    concept_A_backlinks = set(backlinks_dict.get(row['A'], []))
    concept_B_backlinks = set(backlinks_dict.get(row['B'], []))

    # 计算不同的backlinks数量
    unique_A_backlinks = concept_A_backlinks - concept_B_backlinks
    unique_B_backlinks = concept_B_backlinks - concept_A_backlinks
    common_backlinks = concept_A_backlinks & concept_B_backlinks

    p_c1 = (len(unique_A_backlinks) + 1)/6641740
    p_c2 = (len(unique_B_backlinks) + 1) / 6641740
    p_common = (len(common_backlinks) + 1) / 6641740
    pmi = ((np.log(p_c1) + np.log(p_c2)) / np.log(p_common)) - 1
    if pmi <= 0:
        PMI = 0
    else:
        PMI = pmi
    PMI_count.append(PMI)
    count = count + 1
    print(count)

# 归一化处理
max_value = max(PMI_count)
min_value = min(PMI_count)
PMI_normal = [(i - min_value) / (max_value - min_value) for i in PMI_count]

df = pd.DataFrame(PMI_normal)
df.to_excel("PMI_value.xlsx", header=None, index=None)
