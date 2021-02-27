import pymysql as py
from crawler.user import UserInfo
import time

'''
    数据库分为basic_info, short_comments, long_comments 个表
    用户信息：user='debian-sys-maint', password='aVANykWZnldyXF2Q',
    1. basic_info的表项包括：ID,name,stars,score,comment_number,long_comment_number，分别对应varchar,vachar,int,float,int,int
    2. short_comments的表项包括：ID(varchar15)，user_name(varchar30),user_score(float),user_comment(text), user_ID(varchar(30),user_url(varchar(100)
    3. long_comments的表项包括：同上
    4. user_info表项包括：user_ID(varchar(30)),user_url(varchar(100)),user_name(varchar(30)),register_time(time),is_robot(smallint)
    5. cur_incomes表项包括:ID(varchar(15)),name(varchar(30)),scores(float(2)),incomes(float(2)),dates(datetime),predict_income(float(2))
'''

movie_id = "24733428"

class Processor(object):

    def __init__(self):
        py.install_as_MySQLdb()
        self.connect = py.connect(host="127.0.0.1",
                                 user="debian-sys-maint",
                                 password="aVANykWZnldyXF2Q",
                                 port=3306,
                                 database="douban",
                                 charset='utf8mb4')
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.connect.close()

    def Commment(self, user_name, user_url, user_ID, user_comment, user_score, ID):
        info = str(ID) + "','" + user_name + "'," + str(user_score) \
               + ",'" + user_comment + "','" + user_url + "','" + user_ID + "')"
        print(info)
        user_time = 'null'#UserInfo(user_url)
        user_info = user_name + "','" + user_url + "','" + user_ID + "'," + user_time + ")"
        self.cursor.execute("replace into short_comments "
                            "(ID,user_name,user_score,user_comment, user_url, user_ID) values ('" + info)
        self.cursor.execute("replace into user_info "
                            "(user_name, user_url, user_ID, register_time) values ('" + user_info)
        self.connect.commit()

    def BasicComment(self, ID, name, comment_num, score, tags, long_comment_num=0):
        info = str(ID) + "','" + name + "'," + str(comment_num) + "," + str(score) + "," + str(long_comment_num) + ")"
        self.cursor.execute("replace into basic_info (ID, name, "
                            "comment_number, score, long_comment_number) values ('" + info)
        self.connect.commit()
        for i in tags:
            info = str(ID) + ",'" + str(i.string) + "')"
            print(info)
            self.cursor.execute("replace into Tags(ID, tag) values (" + info)
            self.connect.commit()

    def ReviewComment(self, user_name, user_url, user_ID, user_score, ID):
        info = str(ID) + "','" + user_name + "'," + str(user_score) \
               + ",'" + user_url + "','" + user_ID + "')"
        print(info)
        user_time = UserInfo(user_url)
        user_info = user_name + "','" + user_url + "','" + user_ID + "','" + user_time + "')"
        self.cursor.execute("replace into long_comments "
                            "(ID,user_name,user_score, user_url, user_ID) values ('" + info)
        self.cursor.execute("replace into user_info "
                            "(user_name, user_url, user_ID, register_time) values ('" + user_info)
        self.connect.commit()

    def mBox(self, movie_name, mbox):
        self.cursor.execute("update basic_info set income=" + str(mbox) + " where name='"+str(movie_name)+"'")
        self.connect.commit()

    def mBoxList(self, movie_name, mbox, movie_ID, score):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(timestamp)
        info = str(movie_ID) + "','" + str(movie_name) + "','" + str(timestamp) + "'," + str(score) + "," + str(mbox) + ")"
        print(info)
        self.cursor.execute("insert into cur_income (ID, name, dates, scores, incomes) values('" + info)
        self.connect.commit()

    def MaoyanHistoryMovie(self, movie_name="", allincome=-1, firstday=-1, firstweek=-1, datetime=" ", watchcount=-1, weibo=0):

        info = str(movie_name) + "'," + str(allincome) + "," + str(firstday) + "," + \
               str(firstweek) + ",'" + str(datetime) + "'," + str(weibo) + "," + str(watchcount) + ")"
        self.cursor.execute("replace into historymovie"
                            "(moviename, allbox, firstdaybox, firstweekbox, datetime, weiboeffect, watchcount) values ('" + info)
        self.connect.commit()

    def Actor(self, movie_name, actor1, actor2):
        info = movie_name + "','" + actor1 + "')"
        self.cursor.execute("replace into actor(moviename, actorname) values('" + info)
        info = movie_name + "','" + actor2 + "')"
        self.cursor.execute("replace into actor(moviename, actorname) values('" + info)
        self.cursor.execute("if not exists(select * from actoreffect where actorname='"+actor1
                            + "') insert into actoreffect(actorname) values ('" + actor1 + "')")
        self.cursor.execute("if not exists(select * from actoreffect where actorname='"+actor2
                            + "') insert into actoreffect(actorname) values ('" + actor2 + "')")
        self.connect.commit()