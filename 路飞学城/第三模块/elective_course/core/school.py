#!_*_coding:utf-8_*_


class school:
    def __init__(self,area):
        self.area = area
        self.grade = []
        self.course = []


    def show_grade(self):
        if len(self.grade) == 0:
            print('此校区暂无班级')
        else:
            print('本校区班级：')
            for i in self.grade:
                print(i)

    def show_course(self):
        if len(self.course) == 0:
            print('此校区暂无课程')
        else:
            print('本校区课程：')
            for i in self.course:
                print(i)

# import pickle
# li = []
# SH_ampus = school('SH_ampus')
# BJ_ampus = school('BJ_ampus')
# li.append(SH_ampus)
# li.append(BJ_ampus)
# with open('..\db\school_info','wb') as f:
#     f.write(pickle.dumps(li))