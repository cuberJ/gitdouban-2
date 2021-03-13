# 爬虫启动入口

from crawler.manager import Manager
from crawler.downloader import download
from crawler.parser import *
from crawler.processor import *
import re
import string
import json
import random
import time
import requests


HEADERS={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87'
                  'Safari/537.36',
         'Cookie':"uuid_n_v=v1; uuid=084A0C205AD011EB9801B7C95A8ED85D27C942E7072C4F38979342DCCDC84A25;"
                  " _csrf=8813f293299e6a606892323d8aec33d45bb5f368fe8ed4ec75edae765c74c4d3;"
                  " Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1611113512; "
                  "Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1611113527; "
                  "_lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; "
                  "_lxsdk_cuid=1771dd94269c8-080aa6fea17ecb-7824675c-1fa400-1771dd9426ac8; "
                  "_lxsdk_s=1771dd9426b-626-88e-f22%7C%7C5; "
                  "_lxsdk=084A0C205AD011EB9801B7C95A8ED85D27C942E7072C4F38979342DCCDC84A25; "
                  "__mta=145013259.1611113514071.1611113514071.1611113514071.1"
         }


class Crawler(object):
    movie_id = 0
    base_url = 'https://movie.douban.com/subject/{}/comments?start=300&limit=20&status=P&sort=new_score'.format(movie_id)
    review_base_url = 'https://movie.douban.com/subject/{}/reviews'.format(movie_id)

    def __init__(self):
        self._processor = Processor()

    def start(self, urls):
        """
        启动爬虫方法
        :param urls: 启动URL
        :return: 抓取的URL数量
        """
        number = 0
        # self.SimilarMovies() # 如果需要更新相关电影，再启动这个函数
        with open("document/breaking_point.txt", "r+", encoding="utf-8") as b:
            temp = b.readline()
            if re.match(r"https://.*", temp):
                new_url = temp
                print("url修改为断点", new_url)
                urls[0] = new_url
            b.close()

        self._manager.append_new_urls(urls, self.base_url)

        print(urls)
        self._processor.cursor.execute("select count(*) from short_comments where ID='" + self.movie_id + "'")
        count = self._processor.cursor.fetchall()[0]
        count = int(int(count[0]) / 20)
        print(count)
        while self._manager.has_new_url() and count < 20:
            count += 1
            # time.sleep(random.randint(1, 5))
            new_url = self._manager.get_new_url()
            print('开始下载第{:03}个URL：{}'.format(number, new_url))
            with open("document/breaking_point.txt", "w+", encoding="utf-8") as f:
                f.truncate(0)
                f.write(new_url)
                f.close()
            html = download(new_url)
            if html is None:
                # print('html is empty .')
                continue
            links, results = parse(html, new_url)
            print("xiayiye de url shi", links)
            if len(links) > 0:
                self._manager.append_new_urls(links, self.base_url)
            if len(results) > 0:
                for result in results:
                    self._processor.Commment(user_name=result['author'],
                                             user_url=result['user_url'],
                                             user_ID=result['user_ID'],
                                             user_comment=result['comment'],
                                             user_score=result['star'],
                                             ID=self.movie_id) # user_name, user_url, user_ID, user_comment,user_score, ID
                    # print("database start .......")
            number += 1

        return number

    def start2(self, urls):
        number = 0
        # self.SimilarMovies() # 如果需要更新相关电影，再启动这个函数
        with open("document/long_breaking_point.txt", "r+", encoding="utf-8") as b:
            temp = b.readline()
            if re.match(r"https://.*", temp):
                new_url = temp
                print("url修改为断点", new_url)
                urls[0] = new_url
            b.close()

        self._manager.append_new_urls(urls, self.review_base_url)

        print(urls)
        # time.sleep(100)
        self._processor.cursor.execute("select count(*) from long_comments where ID='" + self.movie_id + "'")
        count = self._processor.cursor.fetchall()[0]
        count = int(int(count[0]) / 20)
        print(count)
        while self._manager.has_new_url() and count < 15:
            count += 1
            time.sleep(random.randint(1, 5))
            new_url = self._manager.get_new_url()
            print('开始下载第{:03}个URL：{}'.format(number, new_url))
            with open("document/long_breaking_point.txt", "w+", encoding="utf-8") as f:
                f.truncate(0)
                f.write(new_url)
                f.close()
            html = download(new_url)
            if html is None:
                print('html is empty .')
                continue
            links, results = Reviews(html, new_url, self.movie_id)
            print("xiayiye de url shi", links, results)
            if links != 0:
                if len(links) > 0:
                    self._manager.append_new_urls(links, self.review_base_url)
                if len(results) > 0:
                    for result in results:
                        self._processor.ReviewComment(user_name=result['author'],
                                                      user_url=result['user_url'],
                                                      user_ID=result['user_ID'],
                                                      user_score=result['star'],
                                                      ID=self.movie_id)  # user_name, user_url, user_ID, user_comment,user_score, ID
                        # print("database start .......")
                number += 1

        return number

    def SimilarMovies(self):
        # 获取所有相似电影推荐的评分，评论数,并且通过伊恩网爬取历史票房数据
        similar_html = download("https://movie.douban.com/subject/{}/".format(self.movie_id))
        similar_html, similar_name = SilimarMovie(similar_html)
        for i in range(len(similar_name)):
            temp_html = download(similar_html[i])
            id = re.findall(r"\d+", similar_html[i])[0]
            print(id, similar_name[i])
            score, comment_num, review, tags = Score(temp_html)
            self._processor.BasicComment(comment_num=comment_num, score=score, long_comment_num=review, tags=tags,
                                         name=similar_name[i], ID=id)


    def DoubanHistoryMovie(self):
        cursor = self._processor.connect.cursor()
        # cursor.execute("select ID, name from basic_info where score is NULL")
        # cursor.execute("with views(ID, counts) as (select ID, count(*) from short_comments group by ID) select ID from views where counts < 380") # 获得了所有尚未在豆瓣查询过的电影名称
        cursor.execute("select ID from basic_info where language is null")
        similar_name = cursor.fetchall()
        print(len(similar_name))
        for i in similar_name:
            sleep(random.randint(1,5))
            self.movie_id = i[0]
            cursor.execute("select name from basic_info where ID='" + self.movie_id + "'")
            movie_name = cursor.fetchall()
            movie_name = movie_name[0][0]
            self.base_url = 'https://movie.douban.com/subject/{}/comments?start=300&limit=20&status=P&sort=new_score'.format(self.movie_id)
            self.review_base_url = 'https://movie.douban.com/subject/{}/reviews'.format(self.movie_id)
            print("当前要爬的电影是：", movie_name, self.movie_id)
            self._manager = Manager(self.review_base_url)
            root_urls = ['?'.join([self.review_base_url, 'start=0'])]
            # sleep(10)
            # self.start2(root_urls)
            href = "https://movie.douban.com/subject/" + self.movie_id + "/"
            print(href)
            temp_html = download(href)
            score, comment_num, review, tags, language, runtime = Score(temp_html)
            actor1, actor2, actor3, leader = ActorInfo(temp_html)
            # sleep(100)
            self._processor.BasicComment(comment_num=comment_num, score=score, long_comment_num=review, tags=tags,
                                         name=movie_name, ID=self.movie_id, runtime=runtime, language=language)
            self._processor.Actor(actor3=actor3, actor2=actor2, actor1=actor1, leader=leader, movie_name=movie_name)
            with open('document/long_breaking_point.txt', 'w+') as f:
                f.write("")
                f.close()


    def mBoxList(self):
        '''
              while True:
            html_main = download("https://piaofang.maoyan.com/box-office?ver=normal")
            html_score = download("https://movie.douban.com/subject/{}/?from=showing".format(movie_id))
            score, mbox = GetmBox(movie_name=movie_name, html_main=html_main, html_score=html_score)
            self._processor.mBoxList(movie_ID=movie_id, movie_name = movie_name, mbox=mbox, score=score)
            time.sleep(300)
        '''
        self.MaoyanHistoryBox()

    def MaoyanHistoryBox(self):
        Boxurl = "http://piaofang.maoyan.com/mdb/rank"
        html_main = download(Boxurl)
        soup = BeautifulSoup(html_main, 'lxml')
        list1 = soup.find_all('script')[2]
        list1 = re.findall(r'AppData.*]', str(list1))[0]
        list1 = re.findall(r"\"data.*]", list1)[0]
        list1 = "{" + list1 + "}}"
        list1 = json.loads(list1)
        data = list1['data']['list']
        count = 1
        baseUrl = "http://piaofang.maoyan.com/movie/"
        for i in data:
            url = baseUrl + str(i['movieId'])
            print(i['movieId'], i['movieName'], count)
            count += 1
            actor_html = download(url)
            actor1, actor2 = actorEffect(actor_html)
            self._processor.Actor(i['movieName'], actor1, actor2)
            sleep(10)
            movie_html = download(url + "/boxshow?")
            allbox, firstweek, firstday, date = Mbox(movie_html)
            url = url + "/wantindex"
            weibo_html = download(url)
            effect = WeiboEffect(weibo_html)
            self._processor.MaoyanHistoryMovie(movie_name=i['movieName'], allincome=allbox, firstday=firstday, firstweek=firstweek, datetime=date, watchcount=effect)
            sleep(2)

    def testrun(self, url):
        # self.mBoxList()
        self.DoubanHistoryMovie()


if __name__ == "__main__":
    crawler = Crawler()
    crawler.testrun(" ")
    # crawler.testrun("https://movie.douban.com/subject/{}/reviews".format(movie_id))
    # time.sleep(100)
    # 同时抓取看过和未看过的链接，两者区别在于status查询参数上
    # root_urls = ['?'.join([review_base_url, 'start=0'])]
                 #'?'.join([base_url, 'start=0&limit=20&sort=time&status=P'])]
    # nums = crawler.start(root_urls)
    # nums = crawler.start2(root_urls)
    # crawler.SimilarMoviesIncome()
    # print('爬虫执行完成，共抓取{}个URL'.format(nums))
