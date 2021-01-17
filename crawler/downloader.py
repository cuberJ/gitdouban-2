import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Cookie': 'bid=0DPZXFj4Ceo; __utma=30149280.332936979.1610848122.1610883989.1610886925.6; __utmc=30149280; __utmz=30149280.1610848122.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; push_noty_num=0; push_doumail_num=0; ll="118186"; _vwo_uuid_v2=D06D8AC593EA3A7A9365376B15964F5FD|acb3753a0fb9392413ed006daf355e59; __utmv=30149280.23062; ap_v=0,6.0; __gads=ID=addc0966a920bdc5-22a1732ec0c5003e:T=1610883989:RT=1610883989:S=ALNI_MZpeGOx15lJ0_t4qC2Ypj1MjC4s5w; __utmb=30149280.11.8.1610887456292; __utmt_t1=1; RT=s=1610887459143&r=https%3A%2F%2Fmovie.douban.com%2F; dbcl2="230621000:xnXYRN5G5fc"; ck=ED1P; __utmt=1'
}


def download(url):
    try:
        # 如果不登录抓取的数据可能会很有限（未证实），这里简化处理认证部分逻辑，直接把我的cookie信息复制过来
        resp = requests.get(url,
                            headers=HEADERS,
                            timeout=5.0)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(e)
    except Exception as e:
        print(e)