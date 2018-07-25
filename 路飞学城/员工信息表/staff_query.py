# _*_coding:utf-8_*_
# created by Alex Li on 10/15/17
from tabulate import tabulate
import os

STAFF_DB = "staff.db" #因为不会变，所以是常量
COLUMN_ORDERS = ['id','name','age','phone','dept','enrolled_date']



def load_db():
    """
    打开db文件，把文件里的数据的每列转换成一个列表
    1,Alex Li,22,13651054608,IT,2013-04-01

    :return: 
    """
    staff_data = { #把文件里的每列添加到下面这些列表里
        'id':[],
        'name':[],
        'age':[],
        'phone':[],
        'dept':[],
        'enrolled_date':[]
    }


    f = open(STAFF_DB,"r",encoding="utf-8")

    for line in f:
        staff_id,name,age,phone,dept,enrolled_date = line.strip().split(',')
        staff_data['id'].append(staff_id)
        staff_data['name'].append(name)
        staff_data['age'].append(age)
        staff_data['phone'].append(phone)
        staff_data['dept'].append(dept)
        staff_data['enrolled_date'].append(enrolled_date)

    #print(staff_data)
    f.close()
    return staff_data


def save_db():
    """sync data back to db each time after editing"""
    f = open("%s_tmp"%STAFF_DB, "w", encoding="utf-8")

    for index,val in enumerate(STAFF_DATA[COLUMN_ORDERS[0]]):
        row = [str(val)]
        for col in COLUMN_ORDERS[1:]:
            row.append(str(STAFF_DATA[col][index]) )

        raw_row = ",".join(row)
        f.write(raw_row+"\n")
    f.close()
    os.rename("%s_tmp"%STAFF_DB,STAFF_DB)


def print_log(msg,msg_type='info'):
    if msg_type == 'error':
        print("\033[31;1mError:%s\033[0m"%msg)
    else:
        print("\033[32;1mInfo:%s\033[0m"%msg)


def syntax_find(query_clause, matched_data):
    """
    
    :param query_clause: eg. find age,name from staff_table 
    :param matched_data: where方法匹配到的数据
    :return: 
    """

    filter_keys = query_clause.split('find')[1].split('from')[0]
    columns = [i.strip()  for i in filter_keys.split(',')] #要过滤出来的字段
    if "*" in columns:
        if len(columns) == 1: #只有find * from ...成立，*不能与其它字段同时出现
            columns = COLUMN_ORDERS
        else:
            print_log("*不能同时与其它字段出现","error")
            return False
    if len(columns) == 1:
        if not columns[0]:
            print_log("语法错误，find和from之间必须跟字段名或*","error")
            return False
    filtered_data = []
    for index,val in enumerate(matched_data[columns[0]]): #拿要查找的多列的第一个元素，[name,age,dept]，拿到name，到数据库匹配，然后按这一列的每个值 的索引到其它列表里依次找
        row = [val,]
        #if columns[1:]: #代表是多列过滤
        for col in columns[1:]:
            row.append(matched_data[col][index])
        #print("row",row)
        filtered_data.append(row)

    print(tabulate(filtered_data,headers=columns,tablefmt="grid"))
    print_log("匹配到%s条纪录"%len(filtered_data))


def syntax_add(query_clause, matched_data):
    """
    sample: add staff Alex Li,25,134435344,IT,2015-10-29
    :param query_clause: add staff Alex Li,25,134435344,IT,2015-10-29
    :param matched_data: 
    :return: 
    """
    column_vals = [ col.strip() for col in query_clause.split("values")[1].split(',')]
    #print('cols',column_vals)
    if len(column_vals) == len(COLUMN_ORDERS[1:]): #不包含id,id是自增

        #find max id first , and then plus one , becomes the  id of this new record
        init_staff_id = 0
        for i in STAFF_DATA['id']:
            if int(i) > init_staff_id:
                init_staff_id = int(i)

        init_staff_id += 1 #当前最大id再+1
        STAFF_DATA['id'].append(init_staff_id)
        for index,col in enumerate(COLUMN_ORDERS[1:]):
            STAFF_DATA[col].append( column_vals[index] )

    else:
        print_log("提供的字段数据不足，必须字段%s"%COLUMN_ORDERS[1:],'error')

    print(tabulate(STAFF_DATA,headers=COLUMN_ORDERS))
    save_db()
    print_log("成功添加1条纪录到staff_table表")


def syntax_update(query_clause, matched_data):
    pass


def syntax_delete(query_clause, matched_data):
    pass

def op_gt(q_name,q_condtion):
    """
    find records q_name great than q_condtion 
    :param q_name: 查找条件key
    :param q_condtion: 查找条件value
    :return: 
    """
    matched_data = {} #把符合条件的数据都放这
    for k in STAFF_DATA:
        matched_data[k] = []

    q_condtion = float(q_condtion)
    for index,i in enumerate(STAFF_DATA[q_name]):
        if float(i) > q_condtion :
            for k in matched_data:
                matched_data[k].append( STAFF_DATA[k][index] )  #把匹配的数据都 添加到matched_data里

    #print("matched:",matched_data)

    return matched_data

def op_lt():
    """
    less than
    :return: 
    """

def op_eq():
    """
    equal 
    :return: 
    """

def op_like(q_name,q_condtion):
    """
    find records where q_name like q_condition
    :param q_name: 查找条件key
    :param q_condtion: 查找条件value    
    :return: 
    """
    matched_data = {} #把符合条件的数据都放这
    for k in STAFF_DATA:
        matched_data[k] = []

    for index,i in enumerate(STAFF_DATA[q_name]):
        if  q_condtion  in i :
            for k in matched_data:
                matched_data[k].append( STAFF_DATA[k][index] )  #把匹配的数据都 添加到matched_data里

    #print("matched:",matched_data)

    return matched_data

def syntax_where(clause):
    """
    解析where条件，并查询数据
    :param clause: where条件 , eg. name=alex
    :return: False or matched data dict 
    """

    query_data = {} #存储查询出来的结果
    operators = {'>':op_gt,
                 '<':op_lt,
                 '=':op_eq,
                 'like':op_like}
    query_condtion_matched = False #如果匹配语句都没匹配上
    for op_key,op_func in operators.items():
        if op_key in clause:
            q_name,q_condition = clause.split(op_key)
            #print("query:",q_name,q_condition)
            if q_name.strip() in STAFF_DATA:
                matched_data = op_func(q_name.strip(),q_condition.strip()) #调用对应的方法
                return matched_data
            else:
                print_log("字段'%s' 不存在!"%q_name,'error')
                return False

    if not query_condtion_matched:
        print("\033[31;1mError:语句条件%s不支持\033[0m"%clause)
        return False







def syntax_parser(cmd):
    """
    解析语句
    :return: 
    """
    syntax_list = {
        'find':syntax_find,
        'add':syntax_add,
        'update':syntax_update,
        'delete':syntax_delete,
    }
    if cmd.split()[0] in ['find','add','update','delete'] and "staff_table" in cmd :

        if 'where' in cmd:
            query_cmd,where_clause = cmd.split("where")

            matched_data = syntax_where(where_clause.strip())
            if matched_data: #有匹配结果
                action_name = cmd.split()[0]
                syntax_list[action_name](query_cmd,matched_data) #调用对应的action方法
        else:
            syntax_list[cmd.split()[0]](cmd, STAFF_DATA) #没where,使用所有数据


    else:
        print_log('''语法错误!\nsample:[find/add/update/delete] name,age from [staff_table] where [id][>/</=/like][2]''','error')


def main():
    """
    程序主入口
    :return: 
    """

    while True:
        cmd = input("[staff db]:").strip()
        if not cmd:continue

        syntax_parser(cmd)



STAFF_DATA = load_db()

main()