#!/usrbin/env python3
# -*- coding:utf-8 -*-
menu = {
    '北京':{
        '海淀':{
            '五道口':{
                'soho':{},
                '网易':{},
                'google':{}
            },
            '中关村':{
                '爱奇艺':{},
                '汽车之家':{},
                'youku':{},
            },
            '上地':{
                '百度':{},
            },
        },
        '昌平':{
            '沙河':{
                '老男孩':{},
                '北航':{},
            },
            '天通苑':{},
            '回龙观':{},
        },
        '朝阳':{},
        '东城':{},
    },
    '上海':{
        '闵行':{
            "人民广场":{
                '炸鸡店':{}
            }
        },
        '闸北':{
            '火车站':{
                '携程':{}
            }
        },
        '浦东':{},
    },
    '山东':{},
}
floor = menu        #当前层
status_floor = []
while True:
    for i in floor:
        print(i)
    choose = input('input your choice(q退出，r返回上一层):')
    if choose in floor:
        status_floor.append(floor)        #保存所有层的状态
        floor = floor[choose]               #进入下一层
    elif choose == 'r':
        if len(status_floor) > 0:floor = status_floor.pop()     #返回上一层，将最后加入的状态去掉，并将这一层赋值给floor
        else:print('到达顶层')
    elif choose == 'q':break
    else:print('无效的输入')