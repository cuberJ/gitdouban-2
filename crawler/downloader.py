import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                  'Safari/537.36',
    'Cookie': 'll="118186"; bid=si0jzbpvI-4; __utma=30149280.1362564207.1610938321'
              '.1610975181.1610982299.6; __utmc=30149280; __utmz=30149280.1610982299'
              '.6.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utm'
              'cct=/passport/login; __gads=ID=d32ca2d710e4d9b5-225fc955bcc500ae:T=161'
              '0938320:RT=1610938320:S=ALNI_Ma66WM3uDFWcj7od_xUaX9FtNWFAQ; _vwo_uuid'
              '_v2=DFC178517F7FBF8085B42E27614601F49|1951053d6277a61807c7e06ec77d8e7'
              'c; dbcl2="230621000:33/JLvYLcXg"; ck=kunS; push_noty_num=0; push_doum'
              'ail_num=0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1610962765%2C%22h'
              'ttps%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%22%5D; _pk_id.1000'
              '01.8cb4=629008658fdd6abd.1610954732.3.1610962788.1610960006.; __yadk_ui'
              'd=rvnaeAEO0meNXIlzHT8Xa9jnJ8L5LtTC; __utmv=30149280.23062; __utmb=30149280.0.10.1610982299'
}

def download(url):
    try:
        # 如果不登录抓取的数据可能会很有限（未证实），这里简化处理认证部分逻辑，直接把我的cookie信息复制过来
        resp = requests.get(url,
                            headers=HEADERS,
                            timeout=10.0)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(e)
    except Exception as e:
        print(e)