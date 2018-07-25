#!_*_coding:utf-8_*_

import pickle
from core import auth,person
from conf import settings

@auth.auth
def run():
    while True:
        user = auth.get_login_user()
        if user['role'] == 'student':
            with open(settings.USER_FILE, 'rb') as f:
                user_dict = pickle.loads(f.read())
            student = user_dict[user['username']]['username_obj']
            print('*' * 50)
            for i in student.menu:
                print(i)
            print('*' * 50)
            select = input('请输入您的选择(q退出)：').strip()
            if select in student.menu:
                getattr(student,student.menu[select])
            elif select == 'q':break
            else:print('无效的输入')
            user_dict[user['username']]['username_obj'] = student
            with open(settings.USER_FILE, 'wb') as f:
                f.write(pickle.dumps(user_dict))


        elif user['role'] == 'teacher':
            with open(settings.USER_FILE, 'rb') as f:
                user_dict = pickle.loads(f.read())
            teacher = user_dict[user['username']]['username_obj']
            print('*' * 50)
            for i in teacher.menu:
                print(i)
            print('*' * 50)
            select = input('请输入您的选择(q退出)：').strip()
            if select in teacher.menu:
                getattr(teacher,teacher.menu[select])
            elif select == 'q':break
            else:print('无效的输入')
            # user_dict[user['username']]['username_obj'] = teacher
            # with open(settings.USER_FILE, 'wb') as f:
            #     f.write(pickle.dumps(user_dict))


        elif user['role'] == 'manager':
            manager = person.manager(user['username'])
            print('*'*50)
            for i in manager.menu:
                print(i)
            print('*' * 50)
            select = input('请输入您的选择(q退出)：').strip()
            if select in manager.menu:
                getattr(manager,manager.menu[select])
            elif select == 'q':break
            else:print('无效的输入')

