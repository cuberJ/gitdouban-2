import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Cookie': 'bid=QLb1fh3qh2M; _pk_id.100001.4cf6=31a531c64ad63817.1615466294.1.1615466297.1615466294.; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1036349564.1615466295.1615466295.1615466295.1; __utmb=30149280.1.10.1615466295; __utmc=30149280; __utmz=30149280.1615466295.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; dbcl2="226186082:XWtF3j22H8A"'

    # 注意：cookie一定要尽量分段，否则可能会折叠导致latin字符报错。cookie也尽量从文件get_token中复制，其他的文件里的cookie大概率是折叠过的
    # 同时header一定要用Ubuntu浏览器下的，否则也会出现latin报错


}

def download(url):
    try:
        # 如果不登录抓取的数据可能会很有限（未证实），这里简化处理认证部分逻辑，直接把我的cookie信息复制过来
        resp = requests.get(url,
                            headers=HEADERS,
                            timeout=30.0)
        resp.raise_for_status()
        return resp.text# .encode('utf-8')
    except requests.RequestException as e:
        print(e)
    except Exception as e:
        print(e)