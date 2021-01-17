# 爬虫启动入口

from crawler.manager import Manager
from crawler.downloader import download
from crawler.parser import parse
from crawler.processor import Processor
import re
import time

movie_id = 24733428
base_url = 'https://movie.douban.com/subject/{}/comments'.format(movie_id)


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
        with open("breaking_point.txt", "r+", encoding="utf-8") as b:
            temp = b.readline()
            if re.match(r"https://.*", temp):
                new_url = temp
                print("url修改为断点", new_url)
            b.close()
        urls[0] = new_url
        self._manager.append_new_urls(urls)

        print(urls)
        while self._manager.has_new_url():
            time.sleep(2)
            new_url = self._manager.get_new_url()
            print('开始下载第{:03}个URL：{}'.format(number, new_url))
            html = download(new_url)
            if html is None:
                # print('html is empty .')
                continue
            links, results = parse(html, new_url)
            print("xiayiye de url shi", links)
            if len(links) > 0:
                self._manager.append_new_urls(links)
            if len(results) > 0:
                for result in results:
                    self._processor.Commment(user_name=result['author'],
                                             user_url=result['user_url'],
                                             user_ID=result['user_ID'],
                                             user_comment=result['comment'],
                                             user_score=result['star']) # user_name, user_url, user_ID, user_comment,user_score, ID
                    print("database start .......")
            number += 1
            with open("breaking_point.txt", "w+", encoding="utf-8") as f:
                f.truncate(0)
                f.write(new_url)
                f.close()
        return number


if __name__ == "__main__":
    # print("what's the success? what's the failure? what's the life? what's the dream? what's other".replace("'"," "))
    crawler = Crawler()
    # 同时抓取看过和未看过的链接，两者区别在于status查询参数上
    root_urls = [#'?'.join([base_url, 'start=0&limit=20&sort=new_score&status=P']),
                 '?'.join([base_url, 'start=0&limit=20&sort=time&status=P'])]
    nums = crawler.start(root_urls)
    print('爬虫执行完成，共抓取{}个URL'.format(nums))
