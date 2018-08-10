import pymysql
conn=pymysql.connect(host='192.168.0.20',user='wang',password='123',database='db1',charset='utf8')
#游标
cursor=conn.cursor() #执行完毕返回的结果集默认以元组显示
#cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)

name = 'wang'
age = 18
#执行sql语句
# sql='select * from userinfo where name="%s" and password="%s"' %(user,pwd) #注意%s需要加引号
sql='select * from userinfo where name=%s and age=%s'
res=cursor.execute(sql,(name,age)) #执行sql语句，返回sql查询成功的记录数目
print(res)

cursor.close()
conn.close()