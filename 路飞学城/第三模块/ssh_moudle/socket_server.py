import socket
import subprocess
import json
import struct

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  #地址重用
server.bind(('127.0.0.1',6000))
server.listen(5)
print('starting...')
while True:
    conn,addr = server.accept()
    print('客户端地址：',addr)

    while True:
        try:
            data = conn.recv(1024)
            if not data:break
            obj = subprocess.Popen(data.decode('utf-8'),
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            stdout = obj.stdout.read()
            stderr = obj.stderr.read()
            # print(len(stdout)+len(stderr))
            header_dict = {'total_size':len(stdout)+len(stderr)}    #生成报头
            header_json = json.dumps(header_dict)                     #将报头转成字符串
            header_bytes = header_json.encode('utf-8')              #将报头转成字节
            conn.send(struct.pack('i',len(header_bytes)))
            conn.send(header_bytes)
            conn.send(stdout)
            conn.send(stderr)
        except ConnectionResetError:
            break
    conn.close()
server.close()