import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                  'Safari/537.36',
    'Cookie': '__mta=55361172.1609317296162.1614256759186.1614256791658.15; __mta=55361172.1609317296162.'
              '1614255198120.1614256743889.5; _lxsdk_cuid=176b2c927f6c8-02ecb602b6816-5a301e44-144000-176b2c927f6c8; '
              '_lxsdk=E39604D04A7911EB91B6516866DCC349809EF005276E494FB4E4B680791C8200; '
              'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1609317296,1609317320,1611113357; '
              '__mta=55361172.1609317296162.1609317320550.1611113383247.3; theme=moviepro; '
              '__mta=55361172.1609317296162.1614256243011.1614256586577.28;'
              ' _lx_utm=utm_source=baidu&utm_medium=organic&utm_term=%E7%8C%AB%E7%9C%BC;'
              ' _lxsdk_s=177d919208a-ede-ee6-dbf||114'
}

def download(url):
    try:
        # 如果不登录抓取的数据可能会很有限（未证实），这里简化处理认证部分逻辑，直接把我的cookie信息复制过来
        resp = requests.get(url,
                            headers=HEADERS,
                            timeout=10.0)
        resp.raise_for_status()
        return resp.text.encode('utf-8')
    except requests.RequestException as e:
        print(e)
    except Exception as e:
        print(e)