from bs4 import BeautifulSoup
import requests
import sys
import random

def getcookiestr(path):
    '''
    path:配置文件路径
    '''
    try:
        dicookie = {}
        with open(path + r'cfgcookie.txt', 'r') as r:
            inputstr = r.read()
            for one in inputstr.split('; '):
                dicookie[one.split('=')[0]] = one.split('=')[1]
        return dicookie
    except Exception as e:
        print (str(e))
        print (u'请检查cfgcookie.txt配置文件正确性！')

proxy_list = [
    '122.152.226.243:7777',
    '122.51.105.60:7777',
    '106.54.219.218:7777',
    '22.93.92.250:8118',
    '139.129.238.1:8011',
    '119.126.90.50:8118',
    '39.88.47.83:8118',
    '120.78.146.49:9966',
    '114.249.112.65:9000',
    '27.193.49.150:8118',
    '221.199.62.27:8118',
    '120.78.171.14:6666',
    '42.89.212.245:8118',
    '106.13.119.22:8001',
    '117.78.33.45:80',
]


url = 'http://www.dianping.com/hangzhou/ch10'


my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]



headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'Connection',
    'Cookie': 'navCtgScroll=22; _lxsdk_cuid=16e10be6b35c8-03264c75316f12-123b6a5d-1fa400-16e10be6b35c8; _lxsdk=16e10be6b35c8-03264c75316f12-123b6a5d-1fa400-16e10be6b35c8; _hc.v=559c703b-6a82-d4b3-0e88-101ee702c4a4.1572238945; s_ViewType=10; wed_user_path=2784|0; aburl=1; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1572239254; Hm_lpvt_dbeeb675516927da776beeb1d9802bd4=1572239254; cy=3; cye=hangzhou; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16e1147b997-868-95d-66b%7C%7C116',
    'Host': 'www.dianping.com',
    'Referer': 'http://www.dianping.com/hangzhou/ch10/r1666',
    'User-Agent': random.choice(my_headers),
    
}

cookies= getcookiestr('')


requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False

proxy = random.choice(proxy_list)

# r = requests.get(url, headers=headers, cookies=cookies, proxies = {'http': proxy})
# print("object",r)
# with open(r'downloade.html','wb') as w:
#     w.write(r.text.encode('utf-8'))


f = open('downloade.html','r')
data = f.read()
f.close()

soup = BeautifulSoup(data, 'lxml')


title = soup.select_one('title')
try:
    title = title.get_text()
except Exception as e:
    pass


shops = soup.select('.shop-all-list ul li')

for shop in shops:
    picture = shop.select_one('.pic a img')
    picture = picture.get('src').strip()
    print ("shop picture:%s"%(picture))


    title = shop.select_one('.txt .tit h4')
    title = title.get_text().strip()
    print ("shop title:%s"%(title))

    comment = shop.select_one('.txt .comment .sml-rank-stars')
    comment = int(comment.get('class')[1][7:])/10
    print ("shop comment:%s"%(comment))

    addr = shop.select_one('.txt .tag-addr a span')
    addr = addr.get_text().strip()
    print ("shop addr:%s"%(addr))
