import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

ret = requests.get('https://www.autohome.com.cn/news/')
ret.encoding = ret.apparent_encoding      #apparent_encoding检测字符编码，encoding设置字符编码
# print(ret.content)                      #以字节形式打印
# print(ret.text)                         #以字符串形式打印
soup = BeautifulSoup(ret.text,'html.parser')
div = soup.find(name='div',id='auto-channel-lazyload-article')
li_list = div.find_all(name='li')
for li in li_list:
    title = li.find('h3')


    if title:
        src = li.find('img').get('src')
        url = 'https:' + src  # 图片url
        img_name = src.split('__')[1]
        print(title.text)

    # urlretrieve(url, 'photo\{}.jpg'.format(img_name))