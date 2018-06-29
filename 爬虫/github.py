import requests

from bs4 import BeautifulSoup
# github = requests.get(url='https://github.com/login')
#
# print(github.text)
#
# #get请求
# requests.get(url='xxx',     #地址
#              params={},      #传入URL的参数
#              headers={},     #请求头
#              cookies={}      #cookie
#              )               #相当于requests.request(method='get',url='xxx')
# #post请求
# requests.post(url='xxx',
#              params={},
#              headers={},
#              data={},        #数据
#              json={},        #传json格式数据
#              cookies={}
#              )              #相当于requests.request(method='post',url='xxx')
import re,json,os
import google.protobuf
basedir = os.path.dirname(os.path.abspath(__file__))
res_file = os.path.join(basedir,'aa.txt')
print(res_file)

