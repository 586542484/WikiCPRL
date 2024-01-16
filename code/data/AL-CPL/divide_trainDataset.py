import pandas as pd
import numpy as np

df = pd.read_excel('dm_RefD筛选(0.09).xlsx', sheet_name='Sheet2', dtype=int)

# 不在RefD弱标签范围的其他数据
df1 = pd.read_excel('dm_去掉RefD筛选(0.09)数据的其他数据.xlsx', sheet_name='Sheet2', dtype=int)
list1 = df1.values

# label_pos = df.loc[df['result'] == wLabel].to_numpy()
# label_neg = df.loc[df['result'] == 0].to_numpy()

pos_list = df1.loc[df1['result'] == 1].to_numpy()
neg_list = df1.loc[df1['result'] == 0].to_numpy()
pos_idx = list(range(pos_list.shape[0]))
np.random.shuffle(pos_idx)


wlabel_edges = df.values
# print(type(wlabel_edges))
wlabel_edges = wlabel_edges.tolist()
# print(type(wlabel_edges))
err = []

for i in wlabel_edges:
    for j in pos_list:
        if i[0] == j[1] and i[1] == j[0]:
            err.append(i)
            wlabel_edges.remove(i)
wlabel_edges = np.array(wlabel_edges)


wlabel_idx = list(range(wlabel_edges.shape[0]))
np.random.shuffle(wlabel_idx)

train_list1_idx = pos_idx[:93]
other1 = pos_idx[93:180]

train_list2_idx = wlabel_idx[:141]
other2 = wlabel_idx[141:175]

train_edges1 = pos_list[train_list1_idx]
train_edges2 = wlabel_edges[train_list2_idx]

other1_edge = pos_list[other1]
other2_edge = wlabel_edges[other2]

train_edges = []
valtest = []

for i in train_edges1:
    train_edges.append(i)
for i in train_edges2:
    train_edges.append(i)

for j in other1_edge:
    valtest.append(j)
for j in other2_edge:
    valtest.append(j)
for j in neg_list:
    valtest.append(j)

print(len(wlabel_idx))
print(len(other1))
print(len(other2))
print(len(neg_list))

x = pd.DataFrame(train_edges)
y = pd.DataFrame(valtest)
x.to_excel('dm_32_48/ph_train.xlsx', header=None, index=None)
y.to_excel('dm_32_48/val+dm_test.xlsx', header=None, index=None)



# all_edges = df.values
# print(len(all_edges))
# # print(data.shape[0])
#
# pos_idx = list(range(all_edges.shape[0]))
#
# all_edge_idx = list(range(all_edges.shape[0]))  # 0到415
# np.random.shuffle(all_edge_idx)  # 重新排序返回一个随机序列
# train_edge_idx = all_edge_idx[:59]  # 截取边的随机序列列表中，第1到234条边
# train_edges = all_edges[train_edge_idx]  # train_edges为RefD弱标签中随机选出的234条边，用作训练集
#
# list2_index = all_edge_idx[234:416]
# list2 = all_edges[list2_index]
#
# valtest = []
#
# for i in list1:
#     valtest.append(i)
# for i in list2:
#     valtest.append(i)
#
# print(len(valtest))
#
# x = pd.DataFrame(train_edges)
# y = pd.DataFrame(valtest)
# x.to_excel('dm_0_80/ph_train.xlsx', header=None, index=None)
# y.to_excel('dm_0_80/val+dm_test.xlsx', header=None, index=None)
