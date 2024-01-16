import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

df1 = pd.read_csv('dm-bert.csv')
bert_list = list(df1.values)
# print(type(bert_list))
# print(len(bert_list))

df2 = pd.read_excel('data-mining-index.xlsx')
con_index = df2.values
# print(con_index)
# print(len(con_index))

sim = []
for i in con_index:
    A_vec = bert_list[i[0]].reshape(1, -1)
    B_vec = bert_list[i[1]].reshape(1, -1)

    similarity = cosine_similarity(A_vec, B_vec)
    sim.append(similarity)

final_sim = [x.tolist()[0][0] for x in sim]
print(len(final_sim))
print(final_sim)

df = pd.DataFrame(final_sim)
df.to_excel('dm_bert_Sim.xlsx', index=False)
