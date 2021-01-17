import pymysql as py
from crawler.user import UserInfo

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

    def Commment(self, user_name, user_url, user_ID, user_comment,user_score, ID='34962956'):
        info = str(ID) + "','" + user_name + "'," + str(user_score) + ",'" + user_comment + "','" + user_url + "','" + user_ID + "')"
        print(info)
        user_time = UserInfo(user_url)
        user_info = user_name + "','" + user_url + "','" + user_ID + "','" + user_time + "')"
        self.cursor.execute("replace into short_comments (ID,user_name,user_score,user_comment, user_url, user_ID) values ('" + info)
        self.cursor.execute("replace into user_info (user_name, user_url, user_ID, register_time) values ('" + user_info)
        self.connect.commit()
