#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 14:34:30 2019

@author: rain
"""

# 任务： 爬取特定新闻文章的脚本
## duty 1： weixin.qq

import pandas as pd
from bs4 import BeautifulSoup
import requests
old_daily = pd.read_csv('/Users/rain/Desktop/dailies.csv')    # 最原始数据
daily = pd.read_csv('new_daily.csv')   # 处理过的daily 数据
daily = daily.dropna()
## 第一步： 提取特定新闻：
data_weixin = daily[daily.url.str.contains('mp.weixin.qq')]

## 第二步，爬取新闻
contents = []
for i in range(len(data_weixin)):
    try:
        url = 'http://' + data_weixin.url.iloc[i]
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.content, 'html5lib')
        content = soup.find('div',attrs={'class' : 'rich_media_content'})
        content = content.text.strip()
        contents.append(content)
    except:
        contents.append(' ')
    print (i)

## 去掉空行        
data_weixin['content'] = contents
data_weixin = data_weixin[data_weixin.content != ' '].reset_index()
data_weixin.to_csv('wenxin.csv')


# 任务： 爬取特定新闻文章的脚本
import pandas as pd
from bs4 import BeautifulSoup
import requests
daily = pd.read_csv('new_daily.csv')   # 处理过的daily 数据
daily = daily.dropna()
## 第一步： 提取特定新闻：
# duty2: qq
## 第一步： 提取特定新闻：
data_qq = daily[daily.url.str.contains('tech.qq.')].reset_index()

## 第二步，爬取新闻
contents = []
for i in range(len(data_qq)):
    try:
        url = 'https://' + data_qq.url.iloc[i]
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.content, 'html5lib')
        content = soup.find('div',attrs={'class' : 'qq_article'})
        content = content.text.strip()
        contents.append(content)
    except:
        contents.append(' ')
    print (i)

## 去掉空行        
data_qq['content'] = contents
data_qq = data_qq[data_qq.content != ' '].reset_index()
data_qq.to_csv('qq.csv')



## merge

import pandas as pd
weixin = pd.read_csv('weixin.csv')
data = pd.merge(left = data_weixin, right = weixin, on ='id', how = 'inner')
weixin = data[['title_x', 'content_x', 'url_x', 'content_y']]
weixin.rename(columns={'title_x': 'title', 'content_x': 'abstract', 'url_x':'url', 
                       'content_y': 'content'}, inplace=True)
kk = pd.read_csv('kk.csv', header = None)
kk.columns = ['title', 'abstract', 'url', 'content']
sina = pd.read_csv('sina.csv', header = None)
sina.columns = ['title', 'abstract', 'url', 'content']
whole_data = pd.concat([weixin, kk ,sina], axis=0, sort=False)
whole_data = whole_data.drop_duplicates(subset = 'url')

whole_data.to_csv('new_merge.csv')



