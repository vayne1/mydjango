#!_*_coding:utf-8_*_
import pickle
from conf import settings

user_status = False
login_user = {}
def auth(func):     #装饰器验证用户登录
    def inner(*args):
        user_file = settings.USER_FILE
        with open(user_file,'rb') as f:
            user_dict = pickle.loads(f.read().strip())
        global user_status
        if user_status == False:
            print('您为未登录状态，请登录')
            for i in range(3):
                username = input('please input yuor name:').strip()
                if user_dict.get(username):  # 判断用户名是否存在
                    if user_dict[username]['status'] >= 3:  # 判断是否被锁定，status大于等于3即为锁定状态
                        print('输入错误3次，账号被锁定')
                        break
                    else:
                        password = input('please input your password:')  # 判断密码是否正确，正确将status置为0，错误加1
                        if user_dict[username]['pwd'] == password:
                            print('Welcome')
                            user_status = True
                            user_dict[username]['status'] = 0
                            login_user['username'] = username
                            login_user['role'] = user_dict[username]['role']
                            break
                        else:
                            user_dict[username]['status'] += 1
                            print('密码输入错误')
                else:
                    print('用户名不存在')
        if user_status == True:
            return func(*args)
    return inner


def get_login_user():
    return login_user