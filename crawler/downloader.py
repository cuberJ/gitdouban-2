import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Cookie': 'll="118186"; bid=j46iqf_3y3I; _pk_id.100001.4cf6=0359cfe356ced4fc.1615619986.2.1615624158.1615620706.; ap_v=0,6.0; __utma=30149280.963567165.1615619986.1615619986.1615623298.2; __utmc=30149280; __utmz=30149280.1615619986.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1307143809.1615619986.1615619986.1615623298.2; __utmc=223695111; __utmz=223695111.1615619986.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __yadk_uid=rHJOue2O0f9jMWL6mOWAWhwMDiS7klmW; __gads=ID=b786e3ed82b6dd71-22bade8365c6006c:T=1615619986:RT=1615619986:S=ALNI_MbxjKB9DdFRlHT-AghGpyGfHOoitg; _vwo_uuid_v2=D2423FCE93D908094BBB4236265CADA0E|5fdb50179a1d9aea215d37b76b8a3267; _pk_ses.100001.4cf6=*; __utmb=30149280.2.10.1615623298; __utmb=223695111.0.10.1615623298; __utmt=1; dbcl2="226186082:b7nwWEp+Ho0"; ck=7ABA; push_noty_num=0; push_doumail_num=0'

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