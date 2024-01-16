# -*- coding: utf-8 -*-
import pandas as pd

# 得到所有节点的顺序索引
con_list = list(pd.read_csv('concepts.csv', engine='python', encoding='utf-8', header=None)[0])
index1 = []
for i in con_list:
    index1.append(con_list.index(i))
print(index1)
df = pd.DataFrame(index1)
df.to_csv('ind.course.test.index', header=None, index=None)
