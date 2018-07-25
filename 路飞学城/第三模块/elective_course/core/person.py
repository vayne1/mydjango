#!_*_coding:utf-8_*_
import pickle
from conf import settings
from core import course,school
from log import logger

class people:
    def __init__(self,name):
        self.name = name

class teacher(people):
    menu = {'查看个人信息':'get_msg','选择上课班级':'select_grade','查看班级学员':'view_student','修改学员成绩':'update_fraction'}
    def __init__(self,name,):
        super().__init__(name)
        self.school = []

    @property
    def get_msg(self):      #查看个人信息
        print('所在校区：{}'.format(self.school[0].area))
        course_list = []
        with open(settings.GRADE_FILE, 'rb') as f:
            grade_dict = pickle.loads(f.read())
        for i in grade_dict:
            if grade_dict[i].teacher[0].name == self.name:
                course_list.append(i)
        if course_list:
            print('所带班级：')
            for i in course_list:
                print(i)
        else:print('所带班级：无')
        logger.logger('{} view personal information'.format(self.name))


    @property
    def select_grade(self):     #选择上课班级
        course_list = []
        with open(settings.GRADE_FILE, 'rb') as f:
            grade_dict = pickle.loads(f.read())
        print('以下为您所教的班级')
        for i in grade_dict:
            if grade_dict[i].teacher[0].name == self.name:
                course_list.append(i)
                print(i)
        choose = input('选择您要上课的班级：').strip()
        if choose in course_list:
            print('您选择了{}班，去上课吧'.format(choose))
            logger.logger('{} choose class {}'.format(self.name,choose))
        else:print('这不是您教的班级或无此班级')


    @property
    def view_student(self):     #查看班级学员
        course_list = []
        with open(settings.GRADE_FILE, 'rb') as f:
            grade_dict = pickle.loads(f.read())
        with open(settings.USER_FILE, 'rb') as f:
            user_dict = pickle.loads(f.read())
        print('以下为您所教的班级')
        for i in grade_dict:
            if grade_dict[i].teacher[0].name == self.name:
                print(i)
                course_list.append(i)
        choose = input('选择您要查看的班级：').strip()
        if choose in course_list:
            print('班级{}有以下学员：'.format(choose))
            for i in user_dict:
                if user_dict[i]['role'] == 'student':
                    if user_dict[i]['username_obj'].grade[0].name == choose:
                        print(i)
            logger.logger('{} view class {} students'.format(self.name,choose))
        else:print('这不是您教的班级或无此班级')


    @property
    def update_fraction(self):      #修改学员成绩
        course_list = []
        student_list = []
        with open(settings.GRADE_FILE, 'rb') as f:
            grade_dict = pickle.loads(f.read())
        with open(settings.USER_FILE, 'rb') as f:
            user_dict = pickle.loads(f.read())
        print('以下为您所教的班级')
        for i in grade_dict:
            if grade_dict[i].teacher[0].name == self.name:
                print(i)
                course_list.append(i)
        choose = input('选择您要查看的班级：').strip()
        if choose in course_list:
            print('班级{}有以下学员：'.format(choose))
            for i in user_dict:
                if user_dict[i]['role'] == 'student':
                    if user_dict[i]['username_obj'].grade[0].name == choose:
                        print(i)
                        student_list.append(i)
        else:print('这不是您教的班级或无此班级')
        choose1 = input('选择您要修改成绩的学员:').strip()
        if choose1 in student_list:
            choose2 = input('输入学员分数：').strip()
            if choose2.isdigit():choose2 = int(choose2)
            user_dict[choose1]['username_obj'].fraction = choose2
            # print(user_dict[choose1]['username_obj'].fraction,choose2)
            # print(user_dict['student4']['username_obj'].fraction)
            with open(settings.USER_FILE, 'wb') as f:
                f.write(pickle.dumps(user_dict))
            logger.logger('{} Modify student {} performance'.format(self.name,choose1))
            print('修改成绩成功')
        else:print('无此学员或不是本班学员')


class student(people):
    menu = {'查看个人信息':'get_msg','交学费':'put_money','注册':'registered'}
    def __init__(self,name,tuition=False,fraction=None):
        super().__init__(name)
        self.fraction = fraction    #成绩
        self.tuition = tuition      #学费状态
        self.school = []
        self.grade = []

    @property
    def registered(self):       #注册
        if len(self.school) == 0 and len(self.grade) == 0:
            with open(settings.SCHOOL_FILE, 'rb') as f:
                school_list = pickle.loads(f.read())
            for i in school_list:
                print(school_list.index(i), i.area)
            select = input('选择您要报名的校区序号：').strip()
            if select.isdigit() and int(select) in range(len(school_list)):
                self.school.append(i.area)
                for k in school_list[int(select)].grade:
                    print(school_list[int(select)].grade.index(k), k.name)
                select1 = input('选择您要报名的班级序号：').strip()
                if select.isdigit() and int(select) in range(len(school_list)):
                    self.grade.append(school_list[int(select)].grade[int(select1)])
            else:print('无效的输入')
            # print(self.school, self.grade)
            print('注册成功')
            logger.logger('{} successful regist'.format(self.name))
        else:
            print('您已注册过，请勿重复注册')

    @property
    def get_msg(self):      #获取个人信息
        if len(self.school) != 0 and len(self.grade) != 0:
            print('所在校区：{}'.format(self.school[0]))
            print('所选课程：{}'.format(self.grade[0].course[0].name))
            print('所在班级：{}'.format(self.grade[0].name))
            if self.tuition == False:
                print('学费状态：未交学费')
            else:
                print('学费状态：已交学费')
            if self.fraction:
                print('课程成绩：{}'.format(self.fraction))
            else:print('课程成绩：您还没有成绩')
            logger.logger('{} view personal information'.format(self.name))
        else:print('您还未注册')
    @property
    def put_money(self):        #交学费
        if self.tuition == False:
            money = self.grade[0].course[0].price
            print('未交学费,您的课程{}，需要{}'.format(self.grade[0].course[0].name,money))
            self.tuition = True
            print('学费缴纳成功')
            logger.logger('{} successful tuition fee'.format(self.name))
        else:
            print('已交学费')

class manager(people):
    menu = {'创建学员':'create_student','创建讲师':'create_teacher','创建班级':'create_grade','创建课程':'create_course'}
    def __init__(self,name):
        super().__init__(name)

    @property
    def create_student(self):       #创建学生账号
        with open(settings.USER_FILE,'rb') as f:
            user_dict = pickle.loads(f.read())
        username = input('输入学员账号：').strip()
        if user_dict.get(username):
            print('用户名已存在')
            return
        password = input('为学员账号创建密码：').strip()
        username_obj = student(username)
        user_dict[username] = {'pwd':password,'status':0,'role':'student','username_obj':username_obj}
        with open(settings.USER_FILE,'wb') as f:
            f.write(pickle.dumps(user_dict))
        print('创建学员{}账号成功'.format(username))
        logger('{} create an account {}'.format(self.name,username))

    @property
    def create_teacher(self):       #创建讲师账号
        with open(settings.SCHOOL_FILE, 'rb') as f:
            school_list = pickle.loads(f.read())
        with open(settings.USER_FILE,'rb') as f:
            user_dict = pickle.loads(f.read())
        username = input('输入讲师账号：').strip()
        if user_dict.get(username):print('用户名已存在')
        password = input('为讲师账号创建密码：').strip()
        for i in school_list:
            print(school_list.index(i), i.area)
        area = input('请输入讲师所在校区序号').strip()
        if int(area) in range(len(school_list)):
            username_obj = teacher(username)
            username_obj.school.append(school_list[int(area)])      #创建讲师时关联校区
            print('创建讲师{}账号成功'.format(username))
            logger.logger('{} create an account {}'.format(self.name,username))
        else:print('无效的输入')

        user_dict[username] = {'pwd':password,'status':0,'role':'teacher','username_obj':username_obj}
        with open(settings.USER_FILE,'wb') as f:
            f.write(pickle.dumps(user_dict))
        print('创建讲师{}账号成功'.format(username))

    @property
    def create_course(self):        #创建课程
        with open(settings.COURSE_FILE,'rb') as f:
            course_dict = pickle.loads(f.read())
        with open(settings.SCHOOL_FILE, 'rb') as f:
            school_list = pickle.loads(f.read())
        for i in school_list:
            print(school_list.index(i), i.area)
        area = input('请输入创建课程的校区序号').strip()
        if area.isdigit() and int(area) in range(len(school_list)):
            area = school_list[int(area)]
        else:print('无效的输入')
        course_name = input('请输入课程名：').strip()
        course_period = input('请输入课程周期：').strip()
        course_price = input('请输入课程价钱：').strip()
        course_obj = course.course(course_name,course_period,course_price)
        area.course.append(course_name)
        course_dict[course_name] = course_obj
        with open(settings.COURSE_FILE, 'wb') as f:
            f.write(pickle.dumps(course_dict))
        with open(settings.SCHOOL_FILE, 'wb') as f:
            f.write(pickle.dumps(school_list))


    @property
    def create_grade(self):         #创建班级
        teacher_list = []
        with open(settings.GRADE_FILE,'rb') as f:
            grade_dict = pickle.loads(f.read())
        with open(settings.COURSE_FILE,'rb') as f:
            course_dict = pickle.loads(f.read())
        with open(settings.USER_FILE,'rb') as f:
            user_dict = pickle.loads(f.read())
        with open(settings.SCHOOL_FILE, 'rb') as f:
            school_list = pickle.loads(f.read())
        for i in school_list:
            print(school_list.index(i), i.area)
        area_num = input('请输入创建班级的校区序号').strip()
        if area_num.isdigit() and int(area_num) in range(len(school_list)):
            area = school_list[int(area_num)]
        else:print('无效的输入')
        grade_name = input('输入班级名:').strip()
        area.show_course()
        grade_course = input('关联课程:').strip()
        if grade_course not in course_dict:
            print('无此课程')
            return

        for i in user_dict:
            if user_dict[i]['role'] == 'teacher':
                if user_dict[i]['username_obj'].school[0].area == area.area:
                    # print(user_dict[i]['username_obj'].school[0].area,area.area)
                    teacher_list.append(i)
        if teacher_list:
            print('本校区讲师：')
            for i in teacher_list:
                print(i)
        else:
            print('本校区暂无讲师，请先创建讲师')
            return
        grade_teacher = input('关联讲师:').strip()
        if grade_teacher not in user_dict:
            print('无此讲师')
            return
        grade_obj = course.grade(grade_name)
        grade_obj.course.append(course_dict[grade_course])
        grade_obj.teacher.append(user_dict[grade_teacher]['username_obj'])
        # area.grade.append(grade_obj)
        school_list[int(area_num)].grade.append(grade_obj)
        grade_dict[grade_name] = grade_obj
        print('创建班级{}成功'.format(grade_name))
        logger.logger('{} successful create class {}'.format(self.name,grade_name))
        with open(settings.SCHOOL_FILE, 'wb') as f:
            f.write(pickle.dumps(school_list))
        with open(settings.GRADE_FILE, 'wb') as f:
            f.write(pickle.dumps(grade_dict))

