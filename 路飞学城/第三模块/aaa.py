#!/usrbin/env python3
# -*- coding:utf-8 -*-
# class People:
#     def __init__(self,name,age,sex):
#         self.name=name
#         self.age=age
#         self.sex=sex
#
# class Course:
#     def __init__(self,name,period,price):
#         self.name=name
#         self.period=period
#         self.price=price
#     def tell_info(self):
#         print('<%s %s %s>' %(self.name,self.period,self.price))
#
# class Teacher(People):
#     def __init__(self,name,age,sex,job_title):
#         People.__init__(self,name,age,sex)
#         self.job_title=job_title
#         self.course=[]
#         self.students=[]
#
#
# class Student(People):
#     def __init__(self,name,age,sex):
#         People.__init__(self,name,age,sex)
#         self.course=[]
#
#
# egon=Teacher('egon',18,'male','沙河霸道金牌讲师')
# s1=Student('牛榴弹',18,'female')
#
# python=Course('python','3mons',3000.0)
# linux=Course('linux','3mons',3000.0)
#
# #为老师egon和学生s1添加课程
# print(egon.course)
# egon.course.append(python)
# egon.course.append(linux)
# s1.course.append(python)
#
# #为老师egon添加学生s1
# egon.students.append(s1)
#
# #使用
# for obj in egon.course:
#     obj.tell_info()

# class foo:
#     def __init__(self,name):
#         self.name = name
#     def __getitem__(self, item):
#         print(item)
#
#     def tell(self):
#         print('name is %s' %self.name)
#
#     # @classmethod
#     # def func(cls):
#     #     print(cls)
#     #
#     # @staticmethod
#     # def func1(x,y):
#     #     print(x+y)
#
#
# a= foo('aaaa')
# print(foo.__dict__)
# h = getattr(a,'tell')
# h()
# import subprocess
# obj = subprocess.Popen('dir',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
# print(obj.stdout.read().decode('gbk'))
# print(obj.stderr.read().decode('gbk'))

import struct
res = struct.pack('i',1111111111)
print(res,len(res))

a = struct.unpack('i',res)
print(a)













