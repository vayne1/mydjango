#!/usrbin/env python3
# -*- coding:utf-8 -*-

import json


# user_dict = {'wang':{'pwd':'123','status':0},
#              'hello':{'pwd':'456','status':0},
#              'haha':{'pwd':'789','status':0},
#              }

with open('user.txt','r') as f:             #将用户信息状态加载到内存中
    user_dict = json.loads(f.read())
for i in range(3):
    username = input('please input yuor name:')
    if user_dict.get(username):                 #判断用户名是否存在
       if user_dict[username]['status'] >= 3:   #判断是否被锁定，status大于等于3即为锁定状态
           print('输入错误3次，账号被锁定')
           break
       else:
           password = input('please input your password:')  #判断密码是否正确，正确将status置为0，错误加1
           if user_dict[username]['pwd'] == password:   
               print('Welcome')
               user_dict[username]['status'] = 0
               break
           else:
               user_dict[username]['status'] += 1
               print('密码输入错误')
    else:
        print('用户名不存在')

with open('user.txt','w') as f:         #将更新过的用户信息写入文件
    f.write(json.dumps(user_dict))