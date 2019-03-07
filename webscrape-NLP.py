from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
from selenium.webdriver.common.keys import Keys #引入keys类操作
driver = webdriver.Chrome('/Users/rain/Desktop/chromedriver')
driver.get('https://www.jiqizhixin.com/dailies')
import time
import pandas as pd


#  加载网页直到找到2月20（使用click）
time_all=[]
while '2月19' not in time_all:
    time_find=driver.find_elements_by_css_selector('.js-daily-time')
    for ele in time_find:
    month=ele.find_element_by_css_selector('.daily-every__month').text
    day=ele.find_element_by_css_selector('.daily-every__day').text
    if month+day not in time_all:
         time_all.append(month+day)
    driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "u-loadmore__btn", " " ))]').click()
    time.sleep(15)

# 写成function
def util(day):
    """根据所需要的查询截止日期进行网页加载
    day -- 截止查询日期"""
    time_all = []
    while day not in time_all:
        time_find = driver.find_elements_by_css_selector('.js-daily-time')
        for ele in time_find:
            month = ele.find_element_by_css_selector('.daily-every__month').text
        day = ele.find_element_by_css_selector('.daily-every__day').text
        if month + day not in time_all:
            time_all.append(month + day)
        driver.find_element_by_xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "u-loadmore__btn", " " ))]').click()
        time.sleep(15)




# 按照时间抓取每一个版块的信息信息 并构造dataframe
def get_certain_info(Month,Day):
    """在给定查询日期与月份后，将属于该日期的信息构成dataframe
    month day -- 特定日期
    return -- 包含有特定日期的dataframe"""
    Ele_list = driver.find_elements_by_css_selector('.daily-every.js-daily-every')
    for ele in Ele_list:
        month = ele.find_element_by_css_selector('.daily-every__month').text
        if month == Month:
            day = ele.find_element_by_css_selector('.daily-every__day').text
            if day ==Day:
                head = []
                con = []
                item = ele.find_elements_by_css_selector('.daily-every__item')
                for piece in item:
                    heading = piece.find_element_by_css_selector('.js-open-modal').text
                    content = piece.find_element_by_css_selector('.daily__content').text
                    head.append(heading)
                    con.append(content)
                    dic = {'heading': head, 'content': con}
                    df = pd.DataFrame(dic)
    return (df)


# 对于特定日期进行nlp分析
import jieba
import jieba.analyse
stopword=pd.read_fwf('/Users/rain/Desktop/stopword.txt')
from nltk.stem.porter import PorterStemmer

def keyword(data,k):
    """针对dataframe中的每一行进行keywords提取
    k -- 提取的关键词数量"""
    tags=[]
    ps = PorterStemmer()
    for i in range(len(data)):
        review = [ps.stem(word) for word in data.iloc[i, 1] if not word in set(stopword)]
        review = ''.join(review)
        tag = jieba.analyse.extract_tags(review, topK=k, withWeight=True)
        tags.append(tag)
    data['keyword']=pd.Series(tags)
    dataframe=data
    return (dataframe)

# 汇总：针对特定日期，选择特定日期的{文章标题, 文章内容, 主题词List[(主题1, score), (主题2, score), ...]}
def final(Month, Day,k):
    """Month Day -- 所选择的特定时间
    k -- 所需要的关键词个数
    return dataframe"""
    data=get_certain_info(Month, Day)
    dataframe=keyword(data, k)
    return (dataframe)


# 将所有dataframe 按照日期导出csv
data_2_20=final('2月','20',5)
data_2_20.to_csv('data_2_20.csv', encoding='utf_8_sig')
data_2_21=final('2月','21',5)
data_2_21.to_csv('data_2_21.csv', encoding='utf_8_sig')
data_2_22=final('2月','22',5)
data_2_22.to_csv('data_2_22.csv',  encoding='utf_8_sig')
data_2_23=final('2月','23',5)
data_2_23.to_csv('data_2_23.csv', encoding='utf_8_sig')
data_2_24=final('2月','24',5)
data_2_24.to_csv('data_2_24.csv', encoding='utf_8_sig')
data_2_25=final('2月','25',5)
data_2_25.to_csv('data_2_25.csv', encoding='utf_8_sig')
data_2_26=final('2月','26',5)
data_2_26.to_csv('data_2_26.csv', encoding='utf_8_sig')
data_2_27=final('2月','27',5)
data_2_27.to_csv('data_2_27.csv', encoding='utf_8_sig')


# 将所有日期的{文章标题, 文章内容, 主题词List[(主题1, score), (主题2, score), ...]}合并成新dataframe
Data_all=pd.concat([data_2_20,data_2_21,data_2_22,data_2_23,data_2_24,data_2_25,data_2_26,data_2_27])
Data_all.to_csv('data_all.csv',  encoding='utf_8_sig')
str_all=''
for i in range(len(Data_all)):
    str=Data_all.iloc[i,0]+Data_all.iloc[i,1]
    str_all=str_all+str


# 对所有heading + content 进行统计分析，汇总计算出这一周里所有AI Daily快讯的最热门主题
review = [ps.stem(word) for word in str_all if not word in set(stopword)]
review = ''.join(review)
tag = jieba.analyse.extract_tags(review, topK=100, withWeight=True)  # tag为这一周里所有AI Daily快讯的最热门主题：e.g. {(主题1, score), (主题2, score), ...}

#  最后，利用 wordcloud 对这一周里所有AI Daily快讯的最热门主题进行 data visualization
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import codecs
import jieba
import matplotlib.pyplot as plt

# 绘制词云
cloud = WordCloud(
        #设置字体，不指定就会出现乱码
        font_path='/Users/rain/Desktop/simsun.ttc',
        background_color='white',
        max_words=2000,
        max_font_size=80,
    )
cut_text = " ".join(jieba.cut(review))
word_cloud = cloud.generate(cut_text) # 产生词云
plt.imshow(word_cloud)
plt.axis('off')
plt.title('most famous topic on Feb 20 to 27th')
plt.show()