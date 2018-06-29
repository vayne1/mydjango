
import urllib
from urllib import parse,request
from urllib.request import urlretrieve
from  bs4 import BeautifulSoup
import requests
import re
import time



def spider(url):
    response = request.urlopen(url).read().decode()
    soup = BeautifulSoup(response,'html.parser')
    links = soup.find_all('img')
    # print(links)
    all_list = []
    for i in links:
        a = re.split(r' ',str(i))
        all_list.extend(a)
    # print(all_list)
    num = 0
    for i in all_list:

        k = re.search(r'https.*\.jpg', i)
        if k:
            num += 1
            print(k.group())
    print(num)
            # urlretrieve(k.group(),'photo\{}.jpg'.format(num))
    # urllib.urlretrieve(k, "{}.jpg".format(imgID))
# spider('https://www.zhihu.com/question/22918070')
# spider('https://www.zhihu.com/question/29815334')
spider('https://www.zhihu.com/question/269575911')