import pymysql as py
from crawler.user import UserInfo
import time
import csv

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

    def BasicComment(self, ID, name, comment_num, score, tags, language, runtime, long_comment_num=0):
        info = str(ID) + "','" + name + "'," + str(comment_num) + "," + str(score) + "," + str(long_comment_num) + "," + language + "," + runtime + ")"
        self.cursor.execute("replace into basic_info (ID, name, "
                            "comment_number, score, long_comment_number, language, runtime) values ('" + info)
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
        user_time = "null"# UserInfo(user_url)
        user_info = user_name + "','" + user_url + "','" + user_ID + "'," + user_time + ")"
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

    def Actor(self, movie_name, actor1, actor2, actor3, leader):
        info = movie_name + "','" + actor1 + "','" + actor2 + "','" + actor3 + "','" + leader + "')"
        self.cursor.execute("replace into actor(moviename, actorname1, actorname2, actorname3, leader) values('" + info)
        self.cursor.execute("replace into actoreffect(actorname) values ('" + actor1 + "')")
        self.cursor.execute("replace into actoreffect(actorname) values ('" + actor2 + "')")
        self.cursor.execute("replace into actoreffect(actorname) values ('" + actor3 + "')")
        self.cursor.execute("replace into actoreffect(actorname) values ('" + leader + "')")
        self.connect.commit()

    def temp_get(self): # csv序列:ID, movie_name, score, short_comment_num, long_comment_num, short_comment_score, long_comment_score,
        # actor_score, leader_score, ,tags_score, firstday, firstweek, allbox, watch_count, datetime
        '''
        self.cursor.execute("select avg(emotion)*5, ID from short_comments group by ID")
        data = self.cursor.fetchall()
        for movie in data:
            print(movie)
            if movie[0] is None:
                continue
            else:
                self.cursor.execute("update basic_info set short_avg_emotion="+str(movie[0]) + " where ID='" + movie[1] +"'")
        self.connect.commit()
        '''
        '''
        self.cursor.execute("select ID,datetime from basic_info, historymovie where moviename=name")
        datetime = self.cursor.fetchall()
        for date in datetime:
            dates = str(date[1]).split('-')
            score = 0
            if int(dates[0]) > 2010:
                score += int((int(dates[0]) - 2010)/2 + 1)
            dates[1], dates[2] = int(dates[1]), int(dates[2])
            if dates[1] in [7, 8]:
                score += 3
            if dates[1] == 10 and dates[2] in [1, 2, 3, 4, 5, 6, 7]:
                score += 5
            if dates[1] in [1, 2]:
                score += 5
            self.cursor.execute("update basic_info set enviroment=" + str(score) + " where ID='" + date[0] + "'")
        self.connect.commit()
        '''
        '''
        self.cursor.execute("select * from actor")
        names = self.cursor.fetchall()
        for name in names:
            allscore, score = 0, 0
            print(name)
            self.cursor.execute("select actoreffect from actoreffect where actorname='" + name[1] +"'")
            score = int(self.cursor.fetchall()[0][0])
            allscore += score
            self.cursor.execute("select actoreffect from actoreffect where actorname='" + name[3] + "'")
            score = int(self.cursor.fetchall()[0][0])
            allscore += score
            self.cursor.execute("select actoreffect from actoreffect where actorname='" + name[4] + "'")
            score = int(self.cursor.fetchall()[0][0])
            allscore += score
            self.cursor.execute("select actoreffect from actoreffect where actorname='" + name[5] + "'")
            score = int(self.cursor.fetchall()[0][0])
            allscore += score
            self.cursor.execute("update actor set effect=" + str(allscore) + " where moviename='" + name[0] +"'")
        self.connect.commit()
        '''
        '''
        f = open("/mnt/hgfs/杂七杂八的文件/actor1.csv", 'r', encoding='utf-8', newline="")
        reader = csv.reader(f)
        for item in reader:
            print(item)
            if(item[0] == 'Column1'):
                continue
            else:
                self.cursor.execute("update actoreffect set actoreffect=" + str(item[1]) + " where actorname='" + str(item[0]) +"'")
        self.connect.commit()
        '''

        self.cursor.execute("select ID, name, datetime, allbox, firstweekbox, firstdaybox, watchcount, comment_number, long_comment_number, short_avg_emotion, long_avg_score, score, tagscore, enviroment, language, runtime, effect from actor, basic_info, historymovie where name=historymovie.moviename and name = actor.moviename")
        movies = self.cursor.fetchall()
        f = open("/mnt/hgfs/杂七杂八的文件/all_data.csv", 'w', encoding='utf-8', newline="")
        writer = csv.writer(f)
        writer.writerow(['ID', 'name', 'datetime', 'allbox', 'firstweekbox', 'firstdaybox', 'watchcount', 'comment_number', 'long_comment_number', 'short_avg_emotion', 'long_avg_score','score', 'tagscore', 'enviroment', 'isChinese', 'runtime', 'effect'])
        for movie in movies:
            writer.writerow(movie)
            print(movie)



pro = Processor()
pro.temp_get()



