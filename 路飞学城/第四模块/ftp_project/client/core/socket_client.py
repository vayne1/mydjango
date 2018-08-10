import socket,sys,shelve
import json
import struct
import os
import hashlib
from conf import settings
from log import logger

class FTP_client:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    coding = 'utf-8'
    request_queue_size = 5
    def __init__(self,server_addr):
        self.server_addr = server_addr
        self.client = socket.socket(self.address_family,self.socket_type)
        self.client.connect(server_addr)
        self.terminal = None
        # self.shelve_obj = shelve.open('test')

    def client_close(self):
        self.client.close()


    def login(self):
        for i in range(3):
            username = input('input your username:').strip()
            password = input('input your password:').strip()
            if not username or not password:
                print('用户名或密码不能为空')
                continue
            m = hashlib.md5(password.encode(self.coding))
            user_info = {'username':username,'password':m.hexdigest()}
            user_info_json = json.dumps(user_info)
            user_info_bytes = user_info_json.encode(self.coding)
            self.client.send(user_info_bytes)
            res = self.client.recv(1024).decode(self.coding)
            if res == 'not':
                print('用户名密码错误')
                continue
            else:
                logger.logger('{} login successful'.format(username))
                return res


    def run(self):
        user = self.login()
        self.terminal = user
        if user:
            while True:
                cmd = input('{}>>:'.format(self.terminal)).strip()
                if not cmd: continue
                cmd_list = cmd.split()
                if hasattr(self, cmd_list[0]):
                    func = getattr(self, cmd_list[0])
                    func(cmd)
                else:print('无此命令')
        else:
            self.client_close()

    def get(self,cmd):
        if len(cmd.split()) != 2:
            print('参数个数不正确')
            return
        self.client.send(cmd.encode('utf-8'))
        obj = self.client.recv(4)
        header_size = struct.unpack('i',obj)[0]     #获取报头长度
        header_bytes = self.client.recv(header_size)     #报头字节
        header_json = header_bytes.decode('utf-8')  #报头字符串
        header_dict = json.loads(header_json)          #报头字典

        filename = header_dict['filename']
        if filename not in header_dict['file_list']:
            data = self.client.recv(1024)
            print(data.decode(self.coding))
        else:
            # self.shelve_obj[]
            total_size = header_dict['total_size']  # 数据总长度
            progress = self._progress_bar()
            progress.__next__()
            with open('{}\{}'.format(settings.DOWNLOAD_DIR,filename),'wb') as f:
            # print(total_size)
                recv_size = 0
                while recv_size < total_size:       #循环获取数据，直到完成
                    res = self.client.recv(1024)
                    f.write(res)
                    recv_size += len(res)
                    current_percent = recv_size / total_size * 100
                    progress.send(current_percent)

            new_file_md5 = self.get_md5('{}\{}'.format(settings.DOWNLOAD_DIR,filename))
            if new_file_md5 == header_dict['md5']:
                print('\n')
                print('传输完整：{}'.format(new_file_md5))
                logger.logger('get file {} successful'.format(filename))
            else:print('传输过程中有数据丢失')


    def put(self,cmd):
        if len(cmd.split()) != 2:
            print('参数个数不正确')
            return
        file_list = os.listdir(settings.DOWNLOAD_DIR)
        for i in file_list:
            if not os.path.isfile(os.path.join(settings.DOWNLOAD_DIR, i)):
                file_list.pop(file_list.index(i))
        if cmd.split()[1] not in file_list:
            print('此文件不存在')
            return
        self.client.send(cmd.encode('utf-8'))
        self.client.recv(1024)
        filename = cmd.split()[1]
        header_dict = {
            'total_size': os.path.getsize('{}\{}'.format(settings.DOWNLOAD_DIR, filename)),
            'filename': filename,
            'md5': self.get_md5('{}\{}'.format(settings.DOWNLOAD_DIR, filename)),
        }  # 生成报头
        total_size = header_dict['total_size']
        header_json = json.dumps(header_dict)  # 将报头转成字符串
        header_bytes = header_json.encode('utf-8')  # 将报头转成字节
        self.client.send(struct.pack('i', len(header_bytes)))
        self.client.send(header_bytes)
        progress = self._progress_bar()
        progress.__next__()
        judge_quota = self.client.recv(1024).decode(self.coding)
        if judge_quota == 'ok':
            with open('{}\{}'.format(settings.DOWNLOAD_DIR, filename), 'rb') as f:
                send_size = 0
                for i in f:
                    self.client.send(i)
                    send_size += len(i)
                    current_percent = send_size / total_size * 100
                    progress.send(current_percent)

            res = self.client.recv(1024).decode(self.coding)
            if res == 'not':print('上传文件损坏')
            else:
                print('\n')
                print('传输完整：{}'.format(res))
                logger.logger('put file {} successful'.format(filename))
        else:print('空间不足，无法上传')


    def get_md5(self,filename):
        m = hashlib.md5()
        with open(filename,'rb') as f:
            m.update(f.read())
        return m.hexdigest()


    def dir(self,cmd):
        if len(cmd.split()) == 1:
            cmd = cmd+' '+'.'
        elif len(cmd.split()) == 2:
            cmd = cmd
        else:
            print('参数个数不正确')
            return
        self.client.send(cmd.encode(self.coding))
        obj = self.client.recv(4)
        print(obj)
        header_size = struct.unpack('i', obj)[0]  # 获取报头长度
        header_bytes = self.client.recv(header_size)  # 报头字节
        header_json = header_bytes.decode(self.coding)  # 报头字符串
        header_dict = json.loads(header_json)  # 报头字典
        total_size = header_dict['total_size']  # 数据总长度
        # print(total_size)
        recv_size = 0
        recv_data = b''
        while recv_size < total_size:  # 循环获取数据，直到完成
            res = self.client.recv(1024)
            recv_data += res
            recv_size += len(res)
        print(recv_data.decode('gbk'))


    def cd(self,cmd):
        if len(cmd.split()) == 1:
            cmd = cmd+' '+'.'
        elif len(cmd.split()) == 2:
            cmd = cmd
        else:
            print('参数个数不正确')
            return
        self.client.send(cmd.encode(self.coding))
        res = self.client.recv(1024).decode(self.coding)
        if res == 'not':print('此目录不存在')
        else:self.terminal = res


    def pwd(self,cmd):
        if cmd != 'pwd':
            print('参数个数不正确')
            return
        self.client.send(cmd.encode(self.coding))
        obj = self.client.recv(4)
        header_size = struct.unpack('i', obj)[0]  # 获取报头长度
        header_bytes = self.client.recv(header_size)  # 报头字节
        header_json = header_bytes.decode(self.coding)  # 报头字符串
        header_dict = json.loads(header_json)  # 报头字典
        total_size = header_dict['total_size']  # 数据总长度
        # print(total_size)
        recv_size = 0
        recv_data = b''
        while recv_size < total_size:  # 循环获取数据，直到完成
            res = self.client.recv(1024)
            recv_data += res
            recv_size += len(res)
        print(recv_data.decode(self.coding).split('share')[1])

    def _progress_bar(self):
        last_percent = 0
        while True:
            current_percent = yield
            if current_percent >last_percent:
                print('#'*int(current_percent/2)+'{}%'.format(int(current_percent)),end='\r',flush=True)
                last_percent = current_percent

