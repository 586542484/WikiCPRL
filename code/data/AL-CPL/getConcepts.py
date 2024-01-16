import pandas as pd

A_list = list(pd.read_csv(r'D:\Code\PycharmProjects\LK_project\LK_实验改进\词嵌入\AL-CPL\precalculus.csv', header=0)['A'])
B_list = list(pd.read_csv(r'D:\Code\PycharmProjects\LK_project\LK_实验改进\词嵌入\AL-CPL\precalculus.csv', header=0)['B'])
con_list = list(dict.fromkeys(A_list + B_list))

# print(len(con_list))

df = pd.DataFrame(con_list)
df.to_csv('pre_concepts.csv', header=None, index=None)
