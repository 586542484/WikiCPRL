# -*- coding: utf-8 -*-
import pandas as pd
from mediawiki import MediaWiki
wikipedia = MediaWiki()
import json

d = pd.read_csv(r'D:\Code\PycharmProjects\LK_project\MHAVGAE-main\2023-10-15\University course\data\cs_concept_pairs.csv')
A_concepts = d['A'].tolist()
B_concepts = d['B'].tolist()
con_list = list(dict.fromkeys(A_concepts + B_concepts))  # 概念去重(保留顺序)

# 创建一个字典，用于存储每个概念对应的 backlinks 列表
backlinks_dict = {}
count = 0

for i in con_list:
    try:
        # 获取当前概念的backlinks
        backlinks = wikipedia.page(i).backlinks
        # 将概念和对应的 backlinks 列表存入字典
        backlinks_dict[i] = backlinks
    except:
        print("概念" + str(i) + "出现歧义，请输入：")
        x = input()
        backlinks_dict[i] = wikipedia.page(x).backlinks
    count = count + 1
    print(count)

# 将 backlinks_dict 写入文件，JSON格式
with open('backlinks_dict.json', 'w', encoding='utf-8') as json_file:
    json.dump(backlinks_dict, json_file, ensure_ascii=False, indent=4)
