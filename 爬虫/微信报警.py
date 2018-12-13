
import requests
import json
import sys,io
import logging

# sys.stdout = io.TextIOWrapper(sys.stdin.buffer,encoding='utf-8')
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
def logger(msg):
    logging.basicConfig(filename='',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.warning(msg)
corpid = 'ww58e8fcee19ee9c17'
corpsecret = 'W-_sI5-ZyHUdjqKwaqJObhOUs3GeB0_CKJbjLiIqMyM'
get_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(corpid,corpsecret)
headers = {
    'Content-type':'application/json; charset=utf-8'
}
token_json = requests.get(url=get_token_url).text
token_json = json.loads(token_json)
print(token_json)
access_token = token_json['access_token']
msg = '\u0031\u0041发放'

post_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(access_token)
put_msg = {
   "touser" : "@all",
   "toparty" : 1,
   # "totag" : "TagID1 | TagID2",
   "msgtype" : "text",
   "agentid" : 1000002,
   "text" : {
       "content" : msg
   },
   "safe":0
    }
put_msg = json.dumps(put_msg,ensure_ascii = False).encode('utf-8')
res = requests.post(url=post_url,
                    headers=headers,
                    # json=put_msg,
                    data=put_msg,
                    )

print(res.text)
# print(res.encoding)






