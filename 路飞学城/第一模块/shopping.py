#!/usrbin/env python3
# -*- coding:utf-8 -*-
import json,time

goods = [
{"name": "电脑", "price": 1999},
{"name": "鼠标", "price": 10},
{"name": "游艇", "price": 20},
{"name": "美女", "price": 998},
]
def login():        #登录模块
    for i in range(3):
        username = input('please input yuor name:')
        if user_dict.get(username):                 #判断用户名是否存在
           if user_dict[username]['status'] >= 3:   #判断是否被锁定，status大于等于3即为锁定状态
               print('输入错误3次，账号被锁定')
               break
           else:
               password = input('please input your password:')  #判断密码是否正确，正确将status置为0，错误加1
               if user_dict[username]['pwd'] == password:
                   print('\033[32;1mWelcome\033[0m')
                   user_dict[username]['status'] = 0
                   return username
               else:
                   user_dict[username]['status'] += 1
                   print('密码输入错误')
        else:
            print('用户名不存在')

def shopping(username):         #购物模块
    this_time_shop = []         #本次购物列表
    if user_dict[username].get('salary'):   #判断用户是否输入过工资，输入过在字典中取出。
        print('您的余额为\033[32;1m{}\033[0m'.format(user_dict[username]['salary']))
        salary = user_dict[username]['salary']
    else:
        salary = input('请输入您的工资:')
        salary = int(salary)
        user_dict[username]['salary'] = salary
    while True:
        print('*' * 50)
        for thing in goods:     #商品列表，用于退出时打印本次购买的商品
            print('{}.{}\t{}'.format(goods.index(thing),thing['name'],thing['price']))
        print('*' * 50)
        choose = input('\033[34;1m请选择您要买的商品编号（按q退出，s查询消费记录）：\033[0m')
        if choose.isdigit():
            choose = int(choose)
            if int(choose) in range(len(goods)):    #判断驶入编号是否在列表中
                if salary >= goods[choose]['price']:    #判断余额是否能购买此商品
                    this_time_shop.append(goods[choose])
                    now_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                    shop_list = [goods[choose]['name'],goods[choose]['price'],now_time]     #将商品写入文件，用于查询历史记录
                    user_dict[username]['salary'] = salary - goods[choose]['price']         #工资余额写入文件
                    print('\033[32;1m您已购买商品:{}\033[0m'.format(goods[choose]['name']))
                    if user_dict[username].get('shop'):
                        user_dict[username]['shop'].append(shop_list)
                    else:
                        user_dict[username]['shop'] = [shop_list]
            else:
                print('\033[31;1m商品不存在\033[0m')
        elif choose == 'q':     #退出程序
            if len(this_time_shop) > 0:
                print('您本次已购买以下商品：')
                for thing in this_time_shop:
                    print('{}.{}\t{}'.format(this_time_shop.index(thing), thing['name'], thing['price']))
            else:
                print('\033[33;1m您本次没有购买商品\033[0m')
            print('您的余额为\033[32;1m{}\033[0m'.format(user_dict[username]['salary']))
            break
        elif choose == 's':     #查询历史记录
            if user_dict[username].get('shop'):
                print('\033[32;1m以下为您的历史消费记录：\033[0m')
                print('\033[35;1m*\033[0m'*50)
                for i in user_dict[username]['shop']:
                    print(i[0]+'\t'+str(i[1])+'\t'+i[2])
                print('\033[35;1m*\033[0m' * 50)
            else:
                print('\033[36;1m您还没有购买过任何商品\033[0m')
with open('user.txt','r') as f:             #将用户信息状态加载到内存中
    user_dict = json.loads(f.read())
username = login()
shopping(username)
with open('user.txt','w') as f:         #将更新过的用户信息写入文件
    f.write(json.dumps(user_dict))