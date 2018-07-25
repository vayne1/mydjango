#!_*_coding:utf-8_*_

class course:
    def __init__(self,name,period,price):
        self.name = name
        self.period = period
        self.price = price


class grade:
    def __init__(self,name):
        self.name = name
        self.course = []
        self.teacher = []
        # self.student = []



# linux = course('4months','10000')
# python = course('6months','8999')
# go = course('2months','5000')