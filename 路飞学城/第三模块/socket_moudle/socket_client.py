import socket
import json
import struct

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',6000))

while True:
    msg = input('>>:').strip()
    if not msg: continue
    client.send(msg.encode('utf-8'))
    obj = client.recv(4)
    header_size = struct.unpack('i',obj)[0]     #获取报头长度
    header_bytes = client.recv(header_size)     #报头字节
    header_json = header_bytes.decode('utf-8')  #报头字符串
    header_dict = json.loads(header_json)          #报头字典
    total_size = header_dict['total_size']      #数据总长度
    # print(total_size)
    recv_size = 0
    recv_data = b''
    while recv_size < total_size:       #循环获取数据，直到完成
        res = client.recv(1024)
        recv_data += res
        recv_size += len(res)
    print(recv_data.decode('gbk'))
client.close()