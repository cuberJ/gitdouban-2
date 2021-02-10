import jieba.analyse
import pymysql as py
from time import sleep
from snownlp import SnowNLP, seg, sentiment, tag
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

TrainingPath = "/mnt/hgfs/杂七杂八的文件/ratings/ratings.csv"

def GetTrainData(Connect):
    lib = pd.read_csv(TrainingPath)
    poslib = lib[lib.rating == 5].comment
    neglib = lib[lib.rating == 1].comment
    count = 0
    with open("/home/cairenjie/anaconda3/lib/python3.8/site-packages/snownlp/sentiment/pos.txt", "w") as pos_f:
        for i in poslib:
            print(i)
            pos_f.write(str(i) + "\n")
            if count >= 20000:
                break
            count += 1
    count = 0
    with open("/home/cairenjie/anaconda3/lib/python3.8/site-packages/snownlp/sentiment/neg.txt", "w") as neg_f:
        for i in neglib:
            neg_f.write(str(i) + "\n")
            print(i)
            if count >= 20000:
                break
            count += 1
            # sleep(1)
    pos_f.close()
    neg_f.close()

def TrainModel():
    sentiment.train("/home/cairenjie/anaconda3/lib/python3.8/site-packages/snownlp/sentiment/neg.txt",
                    "/home/cairenjie/anaconda3/lib/python3.8/site-packages/snownlp/sentiment/pos.txt")
    sentiment.save("/home/cairenjie/anaconda3/lib/python3.8/site-packages/snownlp/sentiment/shortcomment.marshal")



def JieBaDivide(s1):
    # jieba.load_userdict("TextAnalyse/dict.txt")
    # result = jieba.analyse.extract_tags(s1, topK=False)
    # print(result)
    emotion = SnowNLP(s1)
    return emotion.sentiments

def DataShow(data:list):
    plt.hist(data, bins=np.arange(0, 1, 0.01), facecolor='g')
    plt.xlabel('sentiment')
    plt.ylabel('count')
    plt.show()


def SQLAnalyse():
    py.install_as_MySQLdb()
    connect = py.connect(host="127.0.0.1",
                              user="debian-sys-maint",
                              password="aVANykWZnldyXF2Q",
                              port=3306,
                              database="douban",
                              charset='utf8mb4')
    cursor = connect.cursor()

    cursor.execute("select user_ID, user_score, user_comment from short_comments comments where user_score > 0")
    lib = cursor.fetchall()
    # print(lib[0][2])
    # GetTrainData(connect)
    print("----------------------------------Next Step: Training Model--------------------------------\n\n")
    TrainModel() # 训练专用文本的训练时长大约为一小时
    print(print("----------------------------------Next Step: Judge Text--------------------------------\n\n"))
    f = open("TextAnalyse/analysis.txt", "w")
    f.truncate(0)
    # secTrainLib_pos, secTrainLib_neg = [], []
    highScore_lowSenti, lowScore_highSenti = 0, 0
    print("test1")
    allLib = []
    for i in lib:
        senti = JieBaDivide(i[2])
        allLib.append(senti)
        if i[1] >= 4 and senti < 0.5:
            highScore_lowSenti += 1
            # secTrainLib_pos.append(i[2])
        elif i[1] <= 2 and senti >= 0.5:
            lowScore_highSenti += 1
            # secTrainLib_neg.append(i[2])
        f.write(i[0] + " " + str(senti) + " " + str(i[1]) + " " + i[2] + "\n")
    f.close()
    print("测量值低于实际值的数目为：", highScore_lowSenti)
    print("测量值高于实际值的数目为", lowScore_highSenti)
    print("最终预测正确的比例为:", (len(allLib)-highScore_lowSenti-lowScore_highSenti) / len(allLib))
    DataShow(allLib)
    '''
    with open("/home/cairenjie/anaconda3/lib/python3.8/site-packages/snownlp/sentiment/pos.txt", "a") as pos_f:
        for i in range(len(secTrainLib_pos)):
            # print(secTrainLib_pos[i])
            pos_f.write(secTrainLib_pos[i]+"\n")
    pos_f.close()
    # print("Test:", len(secTrainLib_neg))
    sleep(5)
    with open("/home/cairenjie/anaconda3/lib/python3.8/site-packages/snownlp/sentiment/neg.txt", "a") as neg_f:
        for i in secTrainLib_neg:
            # print(i)
            neg_f.write(i+"\n")
    neg_f.close()
    '''
SQLAnalyse()