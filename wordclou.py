#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 17:13:11 2019

@author: rain
"""

import pandas as pd

data = pd.read_excel('2018-12-05_2019-05-31.xlsx', index_col = None)

#title = [(' '.join((data.title.values)))]
#content = [(' '.join((data.content.values)))]

#data = pd.DataFrame({'title': title, 'content': content})


#  最后，利用 wordcloud 对这一周里所有AI Daily快讯的最热门主题进行 data visualization
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt


df.keywords = df.keywords.map(lambda x: ' '.join(x))

# 对一个list计数
l = list(df.keywords)
from collections import Counter
c = Counter(" ".join(l).split(' '))
c = dict(c)


# 将计数过后的output转成dataframe 
from collections import  OrderedDict
items = sorted(c.items(), key=lambda obj: obj[1], reverse=True)[:150]   # 排序
key = [x[0] for x in items]
value = [x[1] for x in items]
output = pd.DataFrame({'key': key, 'value': value})
output.to_excel('openai 2019-now.xlsx')





df = pd.read_excel('openai 2019-01-至今.xlsx',index_col = None)
dic = df.set_index('key').to_dict()['value']
#df.set_index('ID').T.to_dict('list')    #一列对多列


# 绘制词云
cloud = WordCloud(
        #设置字体，不指定就会出现乱码
        scale=64,
        font_path='simsun.ttc',
        background_color='white',
        max_words=100,
        max_font_size=80,
    )
word_cloud = cloud.generate_from_frequencies(frequencies = dic)
plt.imshow(word_cloud)
plt.axis('off')
plt.title('most famous topics 2019-01-至今')
plt.show()


