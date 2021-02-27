import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Cookie': 'bid=4ZvrHsVQAxk; __utma=30149280.1982148657.1614305304.1614356354.1614388342.7; __utmc=30149280; __utmz=30149280.1614353770.5.3.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; dbcl2="226186082:fJyLU83AJpE"; ck=6GEb; push_noty_num=0; push_doumail_num=0; __utmv=30149280.22618; ll="118186"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1614356352%2C%22https%3A%2F%2Fmovie.douban.com%2Fsubject%2F10440138%2Fcomments%3Fstart%3D40%26limit%3D20%26sort%3Dnew_score%26status%3DP%22%5D; _pk_id.100001.8cb4=ac1dc641689ce708.1614325893.2.1614359970.1614325893.; __gads=ID=937de71efde28be1-22d6cfcc24c6000f:T=1614326356:RT=1614326356:S=ALNI_MZyXU9EqkZ_T0cROHH084wsdmjz5Q; _vwo_uuid_v2=D02D78448D78576FFE797CAA885308AA7|78a90596ffed9a57c5e970e69b1b7b95; __utmb=30149280.1.10.1614388342; __utmt=1; ap_v=0,6.0'

    # 注意：cookie一定要分段，否则可能会折叠导致latin字符报错
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