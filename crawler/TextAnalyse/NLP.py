import pymysql as py
from time import sleep
from snownlp import SnowNLP, seg, sentiment, tag
import pandas as pd
import numpy as np
import jieba
import matplotlib.pyplot as plt

TrainingPath = "/mnt/hgfs/杂七杂八的文件/ratings/ratings.csv"
movie_id = "24733428"
word_counts = []
word_num = 300

with open('stop.txt', 'r', encoding='utf-8') as stop:
    stop_word = set(stop.read().split('\n'))
stop_word.add(" ")


def GetTrainData(Connect):
    lib = pd.read_csv(TrainingPath)
    poslib = lib[lib.rating == 5].comment
    neglib = lib[lib.rating == 1].comment
    count = 0
    with open("/home/cairenjie/anaconda3/lib/python3.8/site-packages/snownlp/sentiment/pos.txt", "w") as pos_f:
        for i in poslib:
            pos_f.write(str(i) + "\n")
            #if count >= 300000:
            #    break
            #count += 1
    count = 0
    with open("/home/cairenjie/anaconda3/lib/python3.8/site-packages/snownlp/sentiment/neg.txt", "w") as neg_f:
        for i in neglib:
            neg_f.write(str(i) + "\n")
            # if count >= 300000:
             #   break
            #count += 1
    pos_f.close()
    neg_f.close()

def TrainModel():
    sentiment.train("/home/cairenjie/anaconda3/lib/python3.8/site-packages/snownlp/sentiment/neg.txt",
                    "/home/cairenjie/anaconda3/lib/python3.8/site-packages/snownlp/sentiment/pos.txt")
    sentiment.save("/home/cairenjie/anaconda3/lib/python3.8/site-packages/snownlp/sentiment/shortcomment.marshal")

def JieBaDivide(s1):
    emotion = SnowNLP(s1)
    return emotion.sentiments

def DataShow(data:list):
    plt.hist(data, bins=np.arange(0, 1, 0.01), facecolor='g')
    plt.xlabel('sentiment')
    plt.ylabel('count')
    plt.show()

def TagAddtoDatabase(connect):
    cursor = connect.cursor()
    exe = "update short_comment set emotion="

def SQLAnalyse():
    py.install_as_MySQLdb()
    connect = py.connect(host="127.0.0.1",
                              user="debian-sys-maint",
                              password="aVANykWZnldyXF2Q",
                              port=3306,
                              database="douban",
                              charset='utf8mb4')
    cursor = connect.cursor()

    cursor.execute("select user_ID, user_score, user_comment from short_comments comments")
    lib = cursor.fetchall()
    GetTrainData(connect)
    print("----------------------------------Next Step: Training Model--------------------------------\n\n")
    # TrainModel() # 训练专用文本的训练时长大约为一小时
    print(print("----------------------------------Next Step: Judge Text--------------------------------\n\n"))
    f = open("TextAnalyse/analysis.txt", "w")
    ftext = open("TextAnalyse/wordCloud.txt", "w")
    f.truncate(0)
    secTrainLib_pos, secTrainLib_neg = [], []
    highScore_lowSenti, lowScore_highSenti = 0, 0
    allLib = []
    dicts = {}
    for i in lib:
        senti = JieBaDivide(i[2])
        if(i[1] > 0):
            allLib.append(senti)
            dicts[i[0]] = senti
        else:
            allLib.append(senti)
            dicts[i[0]] = senti
            if senti >= 0.5:
                secTrainLib_pos.append(senti)
            else:
                secTrainLib_neg.append(senti)
        if i[1] >= 4 and senti < 0.5:
            highScore_lowSenti += 1
            # secTrainLib_pos.append(i[2])
        elif i[1] <= 2 and i[1] > 0 and senti >= 0.5:
            lowScore_highSenti += 1
            # secTrainLib_neg.append(i[2])
        f.write(i[0] + " " + str(senti) + " " + str(i[1]) + " " + i[2] + "\n")
        ftext.write(i[2]+"\n")
        seg_word = jieba.cut(i[2])
        for word in seg_word:
            if word not in stop_word:
                word_counts.append(word)
    f.close()
    ftext.close()
    print("测量值低于实际值的数目为：", highScore_lowSenti)
    print("测量值高于实际值的数目为", lowScore_highSenti)
    print("最终预测正确的比例为:", (len(allLib)-highScore_lowSenti-lowScore_highSenti) / len(allLib))
    print("打分为0的观众中积极的个数为：", len(secTrainLib_pos), "占总人数比例为:", len(secTrainLib_pos)/(len(secTrainLib_pos) + len(secTrainLib_neg)))
    '''
    for key in dicts.keys():
        cursor.execute("update short_comments set emotion="+str(round(dicts[key], 2)) + " where user_id = '" + str(key) + "';")
    connect.commit()
    DataShow(allLib)
    '''
SQLAnalyse()
import wordcloud

from PIL import Image

import collections

print('\n开始制作词云……')                    # 提示当前状态
mask = np.array(Image.open('IMG.JPG'))      # 定义词频背景
wc = wordcloud.WordCloud(
    font_path='NotoSerifCJK-Bold.ttc', # 设置字体（这里选择“仿宋”）
    background_color='white',                   # 背景颜色
    mask=mask,                                # 文字颜色+形状（有mask参数再设定宽高是无效的）
    max_words=word_num,                         # 显示词数
    max_font_size=150                         # 最大字号
)

most_num = collections.Counter(word_counts)
most_num_top = most_num.most_common(word_num)
wc.generate_from_frequencies(most_num)                                        # 从字典生成词云
wc.recolor(color_func=wordcloud.ImageColorGenerator(mask))                       # 将词云颜色设置为背景图方案
plt.figure('词云')                                                               # 弹框名称与大小
plt.subplots_adjust(top=0.99,bottom=0.01,right=0.99,left=0.01,hspace=0,wspace=0) # 调整边距
plt.imshow(wc, interpolation='bilinear')                       # 处理词云
plt.axis('off')                                                                  # 关闭坐标轴
print('制作完成！')                                                             # 提示当前状态
plt.show()