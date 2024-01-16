# 若正例概念对（A,B）存在且同时负例中也有（B,A），那么负例中（B,A）应去除

import pandas as pd

df = pd.read_excel(r'D:\Code\PycharmProjects\LK_project\MHAVGAE-main\semantic_similarity\wLabel(PMI+BERT)\wLabel\train.xlsx', sheet_name='Sheet1')

list_1 = df.loc[df['result'] == 1].to_numpy()
list_0 = df.loc[df['result'] == 0].to_numpy()


list_1 = list_1.tolist()
list_0 = list_0.tolist()

err_0 = []

for i in list_0:
    for j in list_1:
        if i[0] == j[1] and i[1] == j[0]:
            err_0.append(i)

print(len(err_0))
print(err_0)
# print(list_1)
# print(list_0)

