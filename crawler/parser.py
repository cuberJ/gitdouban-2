import datetime
import urllib.parse
import re
import execjs
from time import sleep
from crawler.downloader import download

SCORE = {"还行": 3, "推荐": 4, "力荐": 5, "较差": 2, "很差": 1, "0": 0}


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
    tags = soup.find_all('span', attrs={'property': 'v:genre'})
    TAGS = []
    for i in tags:
        if i.string != "\n":
            TAGS.append(i.string)
    print(TAGS)
    language = soup.find_all('div', attrs={'id': 'info'})[0]
    runtime = language.find_all('span', attrs={'property': 'v:runtime'})[0].string
    runtime = re.findall(r'\d+', runtime)[0]
    # language = language.find_all('span', attrs={'class':'pl'})[6]
    language = re.findall(r'语言:.*<br/>', str(language))[0]
    language = re.split(r'</span> ', language)
    language = re.split(r'<br/>', language[1])[0]
    print(language, runtime)
    if re.match('汉语普通话', language) is None:
        print(language, "changed\n\n")
        language = '0'
    else:
        language = '1'
    review = re.findall(r"\d+", review)[0]
    return score, comments_num, review, tags, language, runtime

def ActorInfo(html):
    soup = BeautifulSoup(html, 'lxml')
    person = soup.find_all('div', attrs={'id': 'info'})[0]
    leader = person.find_all('a', attrs={'rel':'v:directedBy'})[0]
    actors = person.find_all('a', attrs={'rel':'v:starring'})
    print(leader)
    print(actors)
    leader = leader.string
    print(leader, actors[0].string, actors[1].string, actors[2].string)
    return actors[0].string, actors[1].string, actors[2].string, leader

def Reviews(html, url, movie_id):
    soup = BeautifulSoup(html, 'html.parser')

    # 超链接列表
    links = []
    try :
        link = soup.find_all('span', attrs={"class": "next"})[0].find_all('a')[0].get('href')
    except IndexError:
        return 0, 0
    link = "https://movie.douban.com/subject/{}/reviews".format(movie_id) + link
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

def GetMovieidDouban(html):
    # html = open('document/long.html').read()
    soup = BeautifulSoup(html, 'lxml')
    href = soup.find_all('div', attrs={'id': 'wrapper'})[0]
    print(href)
    href = href.find_all('div', attrs={'class': 'item-root'})[0]
    print(href)
    href = href.find_all('a', attrs={'class': "cover-link"})[0].get('href')
    href = re.findall(r'\d+', href)
    print(href)
    return href

# GetMovieidDouban(" ")

def Mbox(html):  # 同时获取三个票房信息及微博影响指数
    soup = BeautifulSoup(html, 'lxml')
    date = soup.find_all('div', attrs={"class": "info-etitle-bar"})[0].get_text()
    date = re.findall(r'\d+-\d+-\d+', date)[0]
    print(date)

    list1 = re.findall(r'AppData.*]', str(soup))[0]
    allbox = re.findall(r'累计综合票房.*\"\d+\.\d\"},{', list1)
    firstdayBox = re.findall(r'首日综合票房.*\"\d+\.\d\"},{', list1)
    firstWeekBox = re.findall(r'首周综合票房.*\"\d+\.\d\"}', list1)
    if len(allbox) > 0:
        allbox = re.findall(r'\d+\.\d', allbox[0])[0]
    else:
        allbox = -1
    if len(firstdayBox) > 0:
        firstdayBox = re.findall(r'\d+\.\d', firstdayBox[0])[0]
    else:
        firstdayBox = -1
    if len(firstWeekBox) > 0:
        firstWeekBox = re.findall(r'\d+\.\d', firstWeekBox[0])[0]
    else:
        firstWeekBox = -1
    print(allbox, firstWeekBox, firstdayBox)
    return allbox, firstWeekBox, firstdayBox, date

def GetmBox(html_main, html_score, movie_name):
    # html_main = download("https://piaofang.maoyan.com/box-office?ver=normal")
    soup = BeautifulSoup(html_main, "lxml")
    list1 = soup.find_all('tr', attrs={'class': re.compile(r'body-row.*')})
    # html_score = download("https://piaofang.maoyan.com/movie/553231/audienceRating?usePageCache=true")
    for item in list1:
        if item.find_all('p', attrs={'class': 'movie-name'})[0].string == movie_name:
            mbox = item.find_all('div', attrs={'class': "boxDesc-wrap red-color"})[0].string
            print("mbox: ", mbox)
            html_score = BeautifulSoup(html_score, "lxml")

            score = html_score.find_all('strong', attrs={'class': 'll rating_num'})[0].string
            print("score:", score)
            return score, mbox
    return 0, 0

def WeiboEffect(html):
    soup = BeautifulSoup(html, 'lxml')
    effect = soup.find_all('div', attrs={"class": "add-want-item-th"})[0]
    effect = effect.find_all('span', attrs={"class": "number"})[0].get_text()
    effect = re.findall(r'\d+', effect)[0]
    print(effect)
    return effect

def actorEffect(html):
    soup = BeautifulSoup(html, 'lxml')
    print(soup)
    actor = soup.find_all('p', attrs={'class': 'title ellipsis-1'})
    print(actor)
    for i in actor:
        i = i.get_text()
    return actor[0], actor[1]