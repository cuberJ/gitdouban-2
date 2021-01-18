import datetime
import urllib.parse
import re
SCORE={"还行": 3, "推荐": 4, "力荐": 5, "较差": 2, "很差": 1, "0": 0}

from bs4 import BeautifulSoup


def parse(html, url):
    soup = BeautifulSoup(html, 'html.parser')

    # 超链接列表
    links = []
    for a in soup.select('#paginator > a'):
        links.append(urllib.parse.urljoin(url, a.get('href')))

    # 数据列表
    results = []
    # 根据 status 参数判断用户是否看过
    is_visit = ('status=P' in url)
    for div in soup.select('#comments > div.comment-item'):
        author = div.select_one('h3 > span.comment-info > a').get_text(strip=True)
        date = div.select_one('h3 > span.comment-info > span.comment-time').get_text(strip=True)
        # rating = div.select_one('h3 > span.comment-info > span.rating')
        # star = 0
        user_url = div.find_all('a')[0].get('href')
        user_ID = user_url.split('/')[-2]
        # if rating is not None:
            # star = rating.get('class')[0].replace('allstar', '')
        stamp = div.find_all('span', class_=re.compile(r"allstar.* rating"))
        if len(stamp) > 0:
            stamp = stamp[0].get('title')  # 获取每个用户的评分,豆瓣存在一部分用户的短评是没有打分的
        else:
            stamp = "0"
        user_score = SCORE[stamp]
        comment = div.select_one('div.comment > p').get_text(strip=True)
        results.append({
            'author': author.replace("'", "\\'"),
            'date': datetime.datetime.strptime(date, '%Y-%m-%d'),
            'star': user_score,
            'comment': comment.replace("'", "\\'"),
            'is_visit': is_visit,
            'user_ID': user_ID,
            'user_url': user_url
        })
    print(results)
    return links, results

def SilimarMovie(html):
    soup = BeautifulSoup(html, 'lxml')
    recommendations = soup.find_all("div", attrs={"class": "recommendations-bd"})[0]
    recommendations = recommendations.find_all("dl")
    similar_url = []
    similar_name = []
    for recom in recommendations:
        href = recom.find_all("a")[0]
        name = recom.find_all("a")[1].string
        href = href.get("href")
        print(href, name)
        similar_url.append(href)
        similar_name.append(name)


    return similar_url, similar_name

def Score(html):
    # html = open("test.html")
    soup = BeautifulSoup(html, 'lxml')
    score = soup.find_all('strong', attrs={'property': 'v:average', 'class': 'll rating_num'})[0].string  # 总平均分
    comments_num = soup.find_all("div", attrs={'class': 'mod-hd'})[0].find_all("a")[1].string
    comments_num = re.findall(r"\d+", comments_num)[0]
    print(comments_num,score)
    review = soup.find_all('section', attrs={'id': 'reviews-wrapper'})[0].find_all('a')[1].string
    tags = soup.find_all('div', attrs={'class': 'tags-body'})[0]
    TAGS = []
    for i in tags:
        if i.string != "\n":
            TAGS.append(i.string)
    review = re.findall(r"\d+", review)[0]
    return score, comments_num, review, tags

def Reviews(html, url):
    soup = BeautifulSoup(html, 'html.parser')

    # 超链接列表
    links = []
    link = soup.find_all('span', attrs={"class": "next"})[0].find_all('a')[0].get('href')
    link = "https://movie.douban.com/subject/24733428/reviews" + link
    links.append(link)

    # 数据列表
    results = []
    # 根据 status 参数判断用户是否看过
    soup = soup.find_all('header', attrs={'class': 'main-hd'})
    for div in soup:
        author = div.find_all('a', attrs={'class': "name"})[0].string
        # date = div.select_one('h3 > span.comment-info > span.comment-time').get_text(strip=True)
        # rating = div.select_one('h3 > span.comment-info > span.rating')
        user_url = div.find_all('a')[0].get('href')
        user_ID = user_url.split('/')[-2]
        #if rating is not None:
            #star = rating.get('class')[0].replace('allstar', '')
        stamp = div.find_all('span', class_=re.compile(r".*main-title-rating"))
        if len(stamp) > 0:
            stamp = stamp[0].get('title')  # 获取每个用户的评分,豆瓣存在一部分用户的短评是没有打分的
        else:
            stamp = "0"
        user_score = SCORE[stamp]
        # comment = div.select_one('div.comment > p').get_text(strip=True)
        results.append({
            'author': author.replace("'", "\\'"),
            'star': user_score,
            # 'comment': comment.replace("'", "\\'"),
            'user_ID': user_ID,
            'user_url': user_url
        })
    for i in results:
        print(i)
    return links, results
