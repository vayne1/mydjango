import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',6000))

while True:
    msg = input('>>:').strip()
    if not msg: continue
    client.send(msg.encode('utf-8'))
    data = client.recv(1024)
    print(data)
client.close()