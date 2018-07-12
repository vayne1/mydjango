#!/usrbin/env python3
# -*- coding:utf-8 -*-

import json,os,re

#注：命令行并没有不区分大小写的功能，只能小写
tables = ['staff_table']
with open('index_info.txt','r') as f:
    index_info = json.loads(f.read())       #每张表的索引以及总列数(除了id列)信息
column_dict = index_info['staff_table']['column']   #字段字典 {"id": 0, "name": 1, "age": 2, "phone": 3, "department": 4, "time": 5}
column_list = list(column_dict.keys())              #字段列表 ['id', 'name', 'age', 'phone', 'department', 'time']



def main_func():    #主函数
    while True:
        user_input = input('Wangsql>')
        if user_input == 'exit':break
        msg_list = user_input.split()
        if set(msg_list).intersection(set(tables)):     #判断表名是否正确
            if msg_list[0] == 'add':
                create(user_input)
            elif msg_list[0] == 'del' and  msg_list[1] == 'from' and  msg_list[3] == 'where':
                delete(user_input)
            elif msg_list[0] == 'update' and msg_list[2] == 'set' and msg_list[4] == 'where':
                update(user_input)
            elif msg_list[0] == 'find' and msg_list[2] == 'from' and msg_list[4] == 'where':
                find(user_input)
            else:
                print('\033[31;1m输入格式错误\033[0m')
        else:
            print('\033[31;1m此表不存在\033[0m')


def create(user_input):     #添加员工记录
    table_name = user_input.split()[1]      #表名
    create_msg = user_input.split('staff_table')[1].split(',')  #员工信息列表
    create_msg[0] = create_msg[0].strip()
    if len(create_msg) == len(index_info['staff_table']['column'])-1:            #判断员工信息参数个数是否正确
        phone_list = []
        with open('{}.txt'.format(table_name),'r',encoding='utf-8') as f:
            for i in f:
                tmp_list = i.strip().split(',')
                phone_list.append(tmp_list[index_info['staff_table']['index']])      #拿到所有电话号码
            last_staff_id = tmp_list[0]             #最后添加的员工信息的staff_id
        if create_msg[2] in phone_list:             #判断要添加的员工电话是否已经存在
            print('\033[31;1m此电话号码已存在\033[0m')
        else:
            create_msg.insert(0,str(int(last_staff_id)+1))
            with open('{}.txt'.format(table_name), 'a', encoding='utf-8') as f:
                f.write(','.join(create_msg)+'\n')
            print('Query OK, 1 row affected')

    else:
        print('\033[31;1m参数错误。(创建员工示例：add table name,age,phone,department,time)\033[0m')

def delete(user_input):     #删除员工记录
    table_name = user_input.split()[2]  #表名
    user_id = user_input.split()[4].split('=')[1]
    tmp_file = '{}_tmp.txt'.format(table_name)
    with open('{}.txt'.format(table_name),'r', encoding='utf-8') as f,open(tmp_file,'a',encoding='utf-8') as F:
        for i in f:
            tmp_list = i.split(',')
            if tmp_list[0] == user_id:continue
            else:F.write(i)
    os.remove('{}.txt'.format(table_name))
    os.rename(tmp_file,'{}.txt'.format(table_name))
    print('Query OK, 1 row affected')


def update(user_input):     #修改员工信息表
    table_name = user_input.split()[1]      #表名
    update_msg = user_input.split('set')[1].split('where')  #输入where前后的信息
    before_arg_list = update_msg[0].split('=')
    after_arg_list = update_msg[1].split('=')
    before_key = before_arg_list[0].strip()     #update staff_table set age=25 where name = "Alex Li"  语句中的age
    before_value = eval(before_arg_list[1].strip()) #update staff_table set age=25 where name = "Alex Li"  语句中的25
    after_key = after_arg_list[0].strip()           #update staff_table set age=25 where name = "Alex Li"  语句中的name
    after_value = eval(after_arg_list[1].strip())   #update staff_table set age=25 where name = "Alex Li"  语句中的Alex Li
    if before_key in column_list and after_key in column_list:  #判断输入语句是否在字段列表中
        tmp_file = '{}_tmp.txt'.format(table_name)
        with open('{}.txt'.format(table_name), 'r', encoding='utf-8') as f, open(tmp_file, 'a', encoding='utf-8') as F:
            n = 0
            for i in f:
                tmp_list = i.strip().split(',')
                if str(after_value) == tmp_list[column_dict[after_key]] and str(before_value) != tmp_list[column_dict[before_key]]: #当name = "Alex Li"并且age不等于25时执行以下代码
                    tmp_list[column_dict[before_key]] = str(before_value)
                    F.write(','.join(tmp_list)+'\n')
                    n += 1
                else:
                    F.write(i)
        os.remove('{}.txt'.format(table_name))
        os.rename(tmp_file, '{}.txt'.format(table_name))
        print('Query OK, {} row affected'.format(n))
    else:print('\033[31;1m参数错误。\033[0m')

def find(user_input):   #匹配查找员工信息
    res_list = []       #将查找之后的信息添加到列表里
    table_name = user_input.split()[3]  # 表名
    find_msg = user_input.split('where')[1].strip() #enroll_date like "2013"    where后面的判断条件
    symbol = re.search('>=|<=|>|<|=|like',find_msg)
    symbol_list = ['=','<','>','>=','<=']
    if symbol.group() == 'like':
        column_key = find_msg.split()[0]        #enroll_date like "2013" 中的enroll_date
        key_word = eval(find_msg.split()[2])    #enroll_date like "2013" 中的2013

        with open('{}.txt'.format(table_name),'r',encoding='utf-8') as f:
            for i in f:
                tmp_list = i.strip().split(',')
                reobj = re.search(key_word,tmp_list[column_dict[column_key]])   #在enroll_date列里匹配带有关键字的行
                if reobj:
                    res_list.append(tmp_list)
    elif symbol.group() in symbol_list:
        column_key = find_msg.split(symbol.group())[0].strip()  #where age>22中age
        key_word = find_msg.split(symbol.group())[1]             #where age>22中22
        if not key_word.isdigit(): key_word = eval(key_word)    #去掉引号，用户输入为dept="IT"
        with open('{}.txt'.format(table_name), 'r', encoding='utf-8') as f:
            for i in f:
                tmp_list = i.strip().split(',')
                if symbol.group() == '=':
                    if tmp_list[column_dict[column_key]] == key_word:
                        res_list.append(tmp_list)
                else:
                    inequality = ''.join([tmp_list[column_dict[column_key]],symbol.group(),str(key_word)])  #拼接不等式为字符串
                    if eval(inequality):
                        res_list.append(tmp_list)

    else:
        print('\033[31;1m没有这个判断条件\033[0m')

    if user_input.split()[1] == '*':
        for i in res_list:
            print(','.join(i))
    else:
        select_list = user_input.split()[1].split(',')      #输入的字段列表： ['name','age']
        if set(select_list).issubset(set(column_list)):     #判断输入的字段是否全在表的字段中
            for i in res_list:
                tmp_list = []
                for k in select_list:
                    tmp_list.append(i[column_dict[k]])
                print(','.join(tmp_list))
        else:print('\033[31;1m此查询字段不存在\033[0m')
    print('Query OK, {} row affected'.format(len(res_list)))


main_func()