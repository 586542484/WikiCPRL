import json
import pandas as pd

from mediawiki import MediaWiki

wikipedia = MediaWiki()
wikipedia.set_api_url(api_url='https://{lang}.wikipedia.org/w/api.php', lang='en')

url = r'D:\Code\PycharmProjects\LK_project\MHAVGAE-main\2023-10-15\University course\data\concepts.csv'

concepts = list(pd.read_csv(url, header=None)[0])

conceptContent_dict = {}
count = 0
for i in concepts:    # 遍历所有概念
    try:
        conceptContent_dict[i] = wikipedia.page(i).content
        count += 1
        print(count)
    except:
        print(i)
        s = input()
        conceptContent_dict[s] = wikipedia.page(s).content
        count += 1
        print(count)

with open(r'D:\Code\PycharmProjects\LK_project\MHAVGAE-main\2023-10-15\University course\BERT\概念content保存\conceptContent.json', 'w') as outfile:
    json.dump(conceptContent_dict, outfile)

# with open(r'D:\Code\PycharmProjects\LK_project\MHAVGAE-main\2023-10-15\LectureBank2\BERT\概念content保存\conceptContent.json', 'rb') as read_file:
#     data = json.load(read_file)

# listall = data.keys()
# print(len(listall))
# print(listall)
#
# for i in concepts:
#     if i not in listall:
#         print(i)
#         s = input()
#         data[i] = data[s]
# #
# # print(len(data))
# with open(r'D:\Code\PycharmProjects\LK_project\MHAVGAE-main\2023-10-15\LectureBank2\BERT\概念content保存\conceptContentAll.json', 'w') as outfile:
#     json.dump(data, outfile)




