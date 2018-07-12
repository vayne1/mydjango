import time,sys,json,re,logging



def log(info):      #记录操作日志
    logging.basicConfig(filename='atm.log',format='%(asctime)s %(message)s', datefmt='%Y-%d-%m %I:%M:%S %p',level=logging.INFO)
    logging.info(info)

def auth(func):     #装饰器验证用户登录
    def inner(*args):
        global username,user_status
        if user_status == False:
            print('您为未登录状态，请登录')
            for i in range(3):
                username = input('please input yuor name:')
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
                            break
                        else:
                            user_dict[username]['status'] += 1
                            print('密码输入错误')
                else:
                    print('用户名不存在')
        if user_status == True:
            return func(*args)
    return inner

@auth
def shop():     #购物
    goods = [
        {"name": "电脑", "price": 1999},
        {"name": "鼠标", "price": 10},
        {"name": "游艇", "price": 20},
        {"name": "美女", "price": 998},
    ]
    this_time_shop = []  # 本次购物列表

    print('您的剩余额度为\033[32;1m{}\033[0m'.format(user_dict[username]['salary']))
    salary = user_dict[username]['salary']
    while True:
        print('*' * 50)
        for thing in goods:  # 商品列表，用于退出时打印本次购买的商品
            print('{}.{}\t{}'.format(goods.index(thing), thing['name'], thing['price']))
        print('*' * 50)
        choose = input('\033[34;1m请选择您要买的商品编号（按q退出，s查询消费记录）：\033[0m')
        if choose.isdigit():
            choose = int(choose)
            if int(choose) in range(len(goods)):  # 判断驶入编号是否在列表中
                if salary >= goods[choose]['price']:  # 判断余额是否能购买此商品
                    this_time_shop.append(goods[choose])
                    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    shop_list = [goods[choose]['name'], goods[choose]['price'], now_time]
                    # user_dict[username]['salary'] = salary - goods[choose]['price']  # 工资余额写入文件
                    msg = credit_card(goods[choose]['price'])      #调用信用卡接口结账
                    print(msg)
                    print('\033[32;1m您已购买商品:{}\033[0m'.format(goods[choose]['name']))
                    if user_dict[username].get('shop_car'):             #将商品加入购物车
                        user_dict[username]['shop_car'].append(shop_list)
                    else:
                        user_dict[username]['shop_car'] = [shop_list]
            else:
                print('\033[31;1m商品不存在\033[0m')
        elif choose == 'q':  # 退出程序
            if len(this_time_shop) > 0:
                print('您本次已购买以下商品：')
                for thing in this_time_shop:
                    print('{}.{}\t{}'.format(this_time_shop.index(thing), thing['name'], thing['price']))
            else:
                print('\033[33;1m您本次没有购买商品\033[0m')
            print('您的剩余额度为\033[32;1m{}\033[0m'.format(user_dict[username]['salary']))
            break
        elif choose == 's':  # 查询历史记录
            if user_dict[username].get('shop'):
                print('\033[32;1m以下为您的历史消费记录：\033[0m')
                print('\033[35;1m*\033[0m' * 50)
                for i in user_dict[username]['shop']:
                    print(i[0] + '\t' + str(i[1]) + '\t' + i[2])
                print('\033[35;1m*\033[0m' * 50)
            else:
                print('\033[36;1m您还没有购买过任何商品\033[0m')

@auth
def expenses_record(): #消费流水
    while True:
        cost = 0
        choose = input('请输入您要查询的月份，本月请按c，全部请按a(只能查本年月份),退出请按q：')
        if choose == 'c':
            month = time.localtime().tm_mon #  本月月份
        elif choose.isdigit() and int(choose) in range(1,13):
            month = choose.strip()
        elif choose == 'a':
            month = ''
        elif choose == 'q':
            break
        else:
            print('无效的输入')
            continue
        print('\033[32;1m以下为您的消费记录：\033[0m')
        print('\033[35;1m*\033[0m' * 50)
        for i in user_dict[username]['shop_car']:
            res = re.search(str(month),i[2].split()[0].split('-')[1])
            if res:
                print(i[0] + '\t' + str(i[1]) + '\t' + i[2])
                cost += i[1]
        print('共计消费：{}'.format(cost))
        print('\033[35;1m*\033[0m' * 50)


@auth
def credit_card(goods_price):  #信用卡结账接口
    salary = user_dict[username]['salary']
    if salary - goods_price >= 0:
        user_dict[username]['salary'] -= goods_price
        log(username+'\t'+'shopping cost {}'.format(goods_price))
        return '扣款成功'
    else:
        return '余额不足'

@auth
def inquire():      #查询信用卡信息
    print('*'*50)
    print('用户名：{}'.format(username))
    print('总额度：{}'.format(user_dict[username]['amount']))
    print('剩余额度：{}'.format(user_dict[username]['salary']))
    print('*' * 50)
    log(username+'\t'+'inquire')

@auth
def withdraw():     #提现
    while True:
        cash = input('请输入您要提款的金额，q退出：')
        if cash.isdigit():
            if int(cash) <= user_dict[username]['salary']:
                all_money = int(cash)+int(cash)*0.05
                user_dict[username]['salary'] -= all_money
                print('取现{}成功，手续费为{}，自动在余额中扣除'.format(int(cash),int(cash)*0.05))
                log(username+'\t'+'withdraw success')
            else:
                print('您的剩余额度不足，请重新输入，q退出')
                log(username+'\t'+'withdraw {} but cash not enough,failed'.format(int(cash)))
        elif cash == 'q':break
        else:print('无效的输入')


@auth
def transfer():     #转账
    while True:
        transfer_user = input('请输入您要转账的账户，q退出：')
        if user_dict.get(transfer_user):
            transfer_cash = input('请输入您要转账的金额：')
            if transfer_cash.isdigit():
                if int(transfer_cash) <= user_dict[username]['salary']:
                    user_dict[username]['salary'] -= int(transfer_cash)
                    user_dict[transfer_user]['salary'] += int(transfer_cash)
                    print('转账成功，请继续操作')
                    log(username+'\t'+'transfer {} to {},success'.format(int(transfer_cash),transfer_user))
                    log(transfer_user+'\t'+'transfer {} from {},success'.format(int(transfer_cash),username))
                else:
                    print('余额不足')
                    log(username+'\t'+'transfer {} but salary not enough,failed'.format(int(transfer_cash)))
            else:print('无效的输入')
        elif transfer_user == 'q':break
        else:print('此账户不存在')

def repayment():        #还款
    pass



def main_func():
    menu = {
        '商城': {
            '购物': {'func':'shop()'},
            '消费流水': {'func':'expenses_record()'},
        },
        'ATM': {
            '查询':{'func':'inquire()'},
            '提现': {'func':'withdraw()'},
            '转账': {'func':'transfer()'},
            '还款': {},
            '操作记录': {},
            '账户管理': {},
        },
    }
    floor = menu  # 当前层
    status_floor = []
    while True:
        print('*' * 50)
        for i in floor:
            print(i)
        print('*' * 50)
        choose = input('input your choice(q退出，b返回上一层):')
        if choose in floor:
            if len(floor[choose]) == 1:
                eval(floor[choose]['func'])
                continue
            status_floor.append(floor)  # 保存所有层的状态
            floor = floor[choose]  # 进入下一层
        elif choose == 'b':
            if len(status_floor) > 0:
                floor = status_floor.pop()  # 返回上一层，将最后加入的状态去掉，并将这一层赋值给floor
            else:
                print('到达顶层')
        elif choose == 'q':
            break
        else:
            print('无效的输入')



print('用户名：wang'.center(50,'-'))
with open('user.txt','r') as f:             #将用户信息状态加载到内存中
    user_dict = json.loads(f.read())
user_status = False

main_func()
# log('aaa')
with open('user.txt','w') as f:         #将更新过的用户信息写入文件
    f.write(json.dumps(user_dict))