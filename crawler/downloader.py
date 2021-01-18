import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                  'Safari/537.36',
    'Cookie': 'll="118186"; bid=si0jzbpvI-4; _pk_id.100001.4cf6=610cf4b42b489254.1610938320.3.1610954814.1610951152.; __'
              'utma=30149280.1362564207.1610938321.1610951152.1610953294.3; __utmc=30149280; __utmz=30149280.1610938321.'
              '1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1208610309.1610938321.1610951152'
              '.1610953294'
              '.3; __utmc=223695111; __utmz=223695111.1610938321.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __'
              'gads=ID=d32ca2d710e4d9b5-225fc955bcc500ae:T=1610938320:RT=1610938320:S=ALNI_Ma66WM3uDFWcj7od_xUaX9FtNWFAQ;'
              ' _vwo_uuid_v2=DFC178517F7FBF8085B42E27614601F49|1951053d6277a61807c7e06ec77d8e7c; __yadk_uid=lcJ6JUTlAyNte'
              'uZtSLnEV7V0M99lHPFz; ap_v=0,6.0; _pk_ses.100001.4cf6=*; __utmb=30149280.3.9.1610954733315; __utmb=223695111'
              '.3.10.1610953294; dbcl2="230621000:H2hqIhYEBvg"; ck=LtlM; push_noty_num=0; push_doumail_num=0; __utmt=1; '
              '__utmv=30149280.23062'
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