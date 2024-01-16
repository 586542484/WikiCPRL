import pandas as pd

# url = "pre_concepts.csv"
# df = pd.read_csv(url, header=None)
# con_list = df[0].tolist()
#
# con_index = []
# for i in con_list:
#     con_index.append(con_list.index(i))
# print(con_index)
# df1 = pd.DataFrame(con_index)
# df1.to_csv('ind.precalculus.test.index', header=None, index=None)

# 将文件中的概念替换成索引值
A_list = list(pd.read_csv(r'D:\Code\PycharmProjects\LK_project\LK_实验改进\词嵌入\AL-CPL\precalculus.csv', encoding='utf-8', header=0)['A'])
B_list = list(pd.read_csv(r'D:\Code\PycharmProjects\LK_project\LK_实验改进\词嵌入\AL-CPL\precalculus.csv', encoding='utf-8', header=0)['B'])
result = list(pd.read_csv(r'D:\Code\PycharmProjects\LK_project\LK_实验改进\词嵌入\AL-CPL\precalculus.csv', encoding='utf-8', header=0)['result'])

con_list = list(pd.read_csv('pre_concepts.csv', encoding='utf-8', header=None)[0])

def get_index(con_list, index_list):
    con_index = []
    for i in con_list:
        for j in index_list:
            if i == j:
                con_index.append(index_list.index(j))
    return con_index
A_index = get_index(A_list, con_list)
B_index = get_index(B_list, con_list)

df = pd.DataFrame({"A": A_index, "B": B_index, "result": result})
df.to_excel('precalculus-originConcepts.xlsx', header=True, index=None)



