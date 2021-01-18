# 爬虫启动入口

from crawler.manager import Manager
from crawler.downloader import download
from crawler.parser import *
from crawler.processor import *
import re
import random
import time

movie_id = 24733428
base_url = 'https://movie.douban.com/subject/{}/comments'.format(movie_id)
review_base_url = 'https://movie.douban.com/subject/{}/reviews'.format(movie_id)


class Crawler(object):

    def __init__(self):
        self._manager = Manager(base_url)
        self._processor = Processor()

    def start(self, urls):
        """
        启动爬虫方法
        :param urls: 启动URL
        :return: 抓取的URL数量
        """
        number = 0
        # self.SimilarMovies() # 如果需要更新相关电影，再启动这个函数
        with open("breaking_point.txt", "r+", encoding="utf-8") as b:
            temp = b.readline()
            if re.match(r"https://.*", temp):
                new_url = temp
                print("url修改为断点", new_url)
                urls[0] = new_url
            b.close()

        self._manager.append_new_urls(urls, base_url)

        print(urls)
        # time.sleep(100)
        while self._manager.has_new_url():
            time.sleep(random.randint(1, 5))
            new_url = self._manager.get_new_url()
            print('开始下载第{:03}个URL：{}'.format(number, new_url))
            with open("breaking_point.txt", "w+", encoding="utf-8") as f:
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
                self._manager.append_new_urls(links, base_url)
            if len(results) > 0:
                for result in results:
                    self._processor.Commment(user_name=result['author'],
                                             user_url=result['user_url'],
                                             user_ID=result['user_ID'],
                                             user_comment=result['comment'],
                                             user_score=result['star']) # user_name, user_url, user_ID, user_comment,user_score, ID
                    # print("database start .......")
            number += 1

        return number

    def start2(self, urls):
        number = 0
        # self.SimilarMovies() # 如果需要更新相关电影，再启动这个函数
        with open("long_breaking_point.txt", "r+", encoding="utf-8") as b:
            temp = b.readline()
            if re.match(r"https://.*", temp):
                new_url = temp
                print("url修改为断点", new_url)
                urls[0] = new_url
            b.close()

        self._manager.append_new_urls(urls, review_base_url)

        print(urls)
        # time.sleep(100)
        while self._manager.has_new_url():
            time.sleep(random.randint(1, 5))
            new_url = self._manager.get_new_url()
            print('开始下载第{:03}个URL：{}'.format(number, new_url))
            with open("long_breaking_point.txt", "w+", encoding="utf-8") as f:
                f.truncate(0)
                f.write(new_url)
                f.close()
            html = download(new_url)
            if html is None:
                print('html is empty .')
                continue
            links, results = Reviews(html, new_url)
            print("xiayiye de url shi", links, results)
            if len(links) > 0:
                self._manager.append_new_urls(links, review_base_url)
            if len(results) > 0:
                for result in results:
                    self._processor.ReviewComment(user_name=result['author'],
                                             user_url=result['user_url'],
                                             user_ID=result['user_ID'],
                                             user_score=result['star'])  # user_name, user_url, user_ID, user_comment,user_score, ID
                    # print("database start .......")
            number += 1

        return number

    def SimilarMovies(self):
        # 获取所有相似电影推荐的评分，评论数
        similar_html = download("https://movie.douban.com/subject/24733428/")
        similar_html, similar_name = SilimarMovie(similar_html)
        for i in range(len(similar_name)):
            temp_html = download(similar_html[i])
            id = re.findall(r"\d+", similar_html[i])[0]
            print(id, similar_name[i])
            score, comment_num, review, tags = Score(temp_html)
            self._processor.BasicComment(comment_num=comment_num, score=score, long_comment_num=review, tags=tags,
                                         name=similar_name[i], ID=id)
        # time.sleep(100)

def testrun(url):
    #html = download(url)
    html = None
    with open("long.html", "r+", encoding="utf-8") as f:
        html = f.read()
        f.close()
    Reviews(html, url)

if __name__ == "__main__":
    # testrun("https://movie.douban.com/subject/24733428/reviews")

    crawler = Crawler()
    # 同时抓取看过和未看过的链接，两者区别在于status查询参数上
    root_urls = ['?'.join([review_base_url, 'start=0'])]
                 #'?'.join([base_url, 'start=0&limit=20&sort=time&status=P'])]
    # nums = crawler.start(root_urls)
    nums = crawler.start2(root_urls)
    print('爬虫执行完成，共抓取{}个URL'.format(nums))
