#特征值12（RefD）
import json

import pandas as pd
import re
import math
from mediawiki import MediaWiki

wikipedia = MediaWiki()
from collections import Counter

wikipedia.set_api_url(api_url='https://{lang}.wikipedia.org/w/api.php', lang='en')

def countRelatedConceptNumbers(s, conceptLinks_dict):
    concept_list = re.findall(r'title="(.*?)">', s) # 概念的链出概念（不去重的）
    # 筛去 findall方法里面有歧义的概念
    filterConcept_list = []
    for j in concept_list:
        if j in conceptLinks_dict:
            filterConcept_list.append(j)
    return dict(Counter(filterConcept_list)) # 统计概念的相关概念数

def read_data():
    url = r"D:\Code\PycharmProjects\LK_project\MHAVGAE-main\2023-10-15\University course\cs_concept_pairs.csv"
    df = pd.read_csv(url)
    g = df['A'].tolist()
    h = df['B'].tolist()
    con_list = list(dict.fromkeys(g + h))  # 概念去重(保留顺序)，避免重复计算
    conceptLinks_dict = {}
    conceptBacklinks_dict = {}
    LinksConceptNumbers_dict = {}
    conceptBackLinksNumbersDict = {}
    count = 0
    for i in con_list:  # 遍历所有概念
        try:
            conceptLinks_dict[i] = wikipedia.page(i).links  # 概念链出
            conceptBacklinks_dict[i] = wikipedia.page(i).backlinks  # 概念链入

            # tf(c,A)
            s = wikipedia.page(i).html
            LinksConceptNumbers_dict[i] = countRelatedConceptNumbers(s, conceptLinks_dict[i])

            # 求概念的相关概念的链入概念数量（dfc）
            for j in conceptLinks_dict[i]:
                if j in conceptBackLinksNumbersDict.keys():  # 避免重复计算
                    pass
                else:
                    try:
                        conceptBackLinksNumbersDict[j] = len(wikipedia.page(j).backlinks)
                    except:
                        conceptBackLinksNumbersDict[j] = 0  # 概念页面不存在
            count += 1
            print(count)
        except:
            print("概念" + str(i) + "出现歧义，请输入：")
            try:
                x = input()
                conceptLinks_dict[i] = wikipedia.page(x).links  # 概念链出
                conceptBacklinks_dict[i] = wikipedia.page(x).backlinks  #概念链入

                # tf(c,A)
                s = wikipedia.page(x).html
                LinksConceptNumbers_dict[i] = countRelatedConceptNumbers(s, conceptLinks_dict[i])

                for j in conceptLinks_dict[i]:  # 求概念的相关概念的链入概念数量（dfc）
                    if j in conceptBackLinksNumbersDict.keys():  # 避免重复计算
                        pass
                    else:
                        try:
                            conceptBackLinksNumbersDict[j] = len(wikipedia.page(j).backlinks)
                        except:
                            conceptBackLinksNumbersDict[j] = -1  # 概念页面不存在

                count += 0
                print(count)
            # {概念,相关概念}字典 {概念,指向概念的链接的词条总数}字典
            except:
                print("概念" + str(i) + "出现歧义，请输入：")
                x = input()
                conceptLinks_dict[i] = wikipedia.page(x).links  # 概念链出
                conceptBacklinks_dict[i] = wikipedia.page(x).backlinks  #概念链入

                # tf(c,A)
                s = wikipedia.page(x).html
                LinksConceptNumbers_dict[i] = countRelatedConceptNumbers(s, conceptLinks_dict[i])

                for j in conceptLinks_dict[i]:  # 求概念的相关概念的链入概念数量（dfc）
                    if j in conceptBackLinksNumbersDict.keys():  # 避免重复计算
                         pass
                    else:
                        try:
                            conceptBackLinksNumbersDict[j] = len(wikipedia.page(j).backlinks)
                        except:
                            conceptBackLinksNumbersDict[j] = -1  # 概念页面不存在
                count += 0
                print(count)
    # {概念,相关概念}字典 {概念,指向概念的链接的词条总数}字典
    with open(r'D:\Code\PycharmProjects\LK_project\MHAVGAE-main\2023-10-15\University course\RefD\files\conceptLinks_dict.json', 'w') as outfile:
        json.dump(conceptLinks_dict, outfile)
    with open(r'D:\Code\PycharmProjects\LK_project\MHAVGAE-main\2023-10-15\University course\RefD\files\conceptBacklinks_dict.json', 'w') as outfile:
        json.dump(conceptBacklinks_dict, outfile)
    with open(r'D:\Code\PycharmProjects\LK_project\MHAVGAE-main\2023-10-15\University course\RefD\files\LinksConceptNumbers_dict.json', 'w') as outfile:
        json.dump(LinksConceptNumbers_dict, outfile)
    with open(r'D:\Code\PycharmProjects\LK_project\MHAVGAE-main\2023-10-15\University course\RefD\files\conceptBackLinksNumbers_dict.json', "w") as outfile:
        json.dump(conceptBackLinksNumbersDict, outfile)
    # with open('C:\shiyan/1111-M2\conceptBacklinks_dict.json', "rb") as read_file:
    # conceptBacklinks_dict = json.load(read_file)
    # with open('C:\shiyan/1111-M2\LinksConceptNumbers_dict.json', "rb") as read_file:
    # LinksConceptNumbers_dict = json.load(read_file)
    # with open('C:\shiyan/1111-M2\LinksConceptNumbers_dict.json', "rb") as read_file:
    # LinksConceptNumbers_dict = json.load(read_file)

    return g, h, conceptBacklinks_dict, LinksConceptNumbers_dict, conceptBackLinksNumbersDict


def RefD_left(conceptBacklinksB_list, conceptNumbersA_dict, conceptLinksBackLinksLength_dict):
    '''
        计算RefD-TF-IDF左半部分的值
        wLabel. 获取 A {相关概念:次数}的字典
        Label_-half. fm : 遍历字典,v*log(N/len(backlinks))
        Label_-all. fz : 对于字典keys,遍历其links，判断B是否存在于links
    Input:
    -----
    A : A 概念
    B : B 概念
    Output:
    -----
    fz/fm : RefD-TF-IDF 左半部分的值
    '''

    sum_fm = 0
    N = 6729507
    for k, v in conceptNumbersA_dict.items():
        if conceptLinksBackLinksLength_dict[k] == 0:
            sum_fm = sum_fm + 0
        else:
            try:
                vi_sum = v * math.log(N / conceptLinksBackLinksLength_dict[k])  # 求有多少词条指向这里
                sum_fm = sum_fm + vi_sum
            except:
                sum_fm = sum_fm + 0
    fm = sum_fm

    sum_1 = 0
    for k, v in conceptNumbersA_dict.items():
        if k in conceptBacklinksB_list and conceptLinksBackLinksLength_dict[k] != 0:
            try:
                sum_1 += v * math.log(N / conceptLinksBackLinksLength_dict[k])
            except:
                sum_1 += 0
        else:
            sum_1 = sum_1 + 0

    fz = sum_1
    if fm == 0:
        return 0
    else:
        return fz / fm


def RefD_right(conceptBacklinksA_list, conceptNumbers_dict, conceptLinksBackLinksLength_dict):
    '''
        计算RefD-TF-IDF右半部分的值
        wLabel. 获取 A {相关概念:次数}的字典
        Label_-half. fm : 遍历字典,v*log(N/len(bancklinks))
        Label_-all. fz : 对于字典keys,遍历其links，判断B是否存在于links
    Input:
    -----
    A : A 概念
    B : B 概念
    Output:
    -----
    fz/fm : RefD-TF-IDF 左半部分的值
    '''

    sum_fm = 0
    N = 6729507
    for k, v in conceptNumbers_dict.items():
        if conceptLinksBackLinksLength_dict[k] == 0:
            sum_fm = sum_fm + 0
        else:
            try:
                vi_sum = v * math.log(N / conceptLinksBackLinksLength_dict[k])  # 求有多少词条指向这里
                sum_fm = sum_fm + vi_sum
            except:
                sum_fm = sum_fm + 0
    fm = sum_fm

    sum_1 = 0
    for k, v in conceptNumbers_dict.items():
        if k in conceptBacklinksA_list and conceptLinksBackLinksLength_dict[k] != 0:
            try:
                sum_1 += v * math.log(N / conceptLinksBackLinksLength_dict[k])
            except:
                sum_1 += 0
        else:
            sum_1 = sum_1 + 0

    fz = sum_1
    if fm == 0:
        return 0
    else:
        return fz / fm


if __name__ == '__main__':
    g, h, conceptBackLinksDict, relatedConceptFrequencyDict, conceptBackLinksNumbersDict = read_data()
    count = 0
    refD_list =[]
    for i, j in enumerate(h):
        A = g[i]  # A概念
        B = j  # B概念
        count += 1
        # RefD_left:
        # wLabel.链入到概念B的 概念集合r(ci,B):conceptBacklinks_dict[B]
        # Label_-half.概念A相关概念和出现次数tf(c,A):LinksConceptNumbers_dict[A]
        # Label_-all.计算连接到概念的次数df(c):conceptLinksBackLinksLength_dict
        sum_l = RefD_left(conceptBackLinksDict[B], relatedConceptFrequencyDict[A], conceptBackLinksNumbersDict)
        sum_r = RefD_right(conceptBackLinksDict[A], relatedConceptFrequencyDict[B], conceptBackLinksNumbersDict)
        print(count, sum_l - sum_r)
        refD_list.append(sum_l-sum_r)

    df = pd.DataFrame.from_dict({'RefD': refD_list})
    df.to_excel(r'D:\Code\PycharmProjects\LK_project\MHAVGAE-main\2023-10-15\LectureBank2\RefD\RefD.xlsx', header=True, index=False)

