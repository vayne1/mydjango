import socket
import os
import json
import struct
import hashlib
import configparser
import subprocess
import queue
from threading import Thread
from conf import settings
from log import logger

# download_dir =r'E:\python\路飞学城\第三模块\ftp_project\server\share'


class RUN:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    coding = 'utf-8'
    request_queue_size = 5

    def __init__(self, server_addr,concurrent_number):
        self.concurrent_number = concurrent_number
        self.server_addr = server_addr
        self.socket = socket.socket(self.address_family, self.socket_type)
        self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 地址重用
        self.socket.bind(server_addr)
        self.socket.listen(self.request_queue_size)


    def close(self):
        self.socket.close()


    @staticmethod
    def _get_config():      #获取配置文件信息
        config = configparser.ConfigParser()
        config.read(settings.CONFIG_FILE)
        return config


    def _get_home_dir(self,username):   #获取用户家目录
        home_dir = os.path.join(os.path.join(settings.BASE_DIR,'share'),username)
        if not os.path.exists(home_dir):
            os.mkdir(home_dir)
        return home_dir


    def _login(self):        #登陆
        config = self._get_config()
        try:
            user_info_bytes = self.conn.recv(1024)
        except ConnectionResetError:
            return
        if user_info_bytes:
            user_info = json.loads(user_info_bytes.decode(self.coding))
            username = user_info['username']
            password = user_info['password']
            if username in config.sections() and password == config[username]['password']:
                self.conn.send(username.encode(self.coding))
                user_dict = {'username':username,'quota':config[username]['quota']}
                logger.logger('{} login successful'.format(username))
                return user_dict
            else:self.conn.send('not'.encode(self.coding))


    def run(self):  # 运行
        print('starting...')
        # self.pool = ThreadPoolExecutor(self.concurrent_number)  # 创建线程池
        q = queue.Queue(self.concurrent_number)     #实例化一个队列
        while True:
            self.conn,self.addr = self.socket.accept()
            print('客户端地址：', self.addr)
            user_dict = self._login()
            if user_dict:
                current_dir = self._get_home_dir(user_dict['username'])
                user_task = FTP_server(self.conn, current_dir)          #创建任务对象
                print('{}登陆成功'.format(user_dict['username']))
                q.put(user_dict, block=True)        #往队列中添加一条数据
                t = Thread(target=user_task.task,args=(user_dict,q,))
                t.start()


class FTP_server:
    coding = 'utf-8'

    def __init__(self,conn,current_dir):
        self.conn = conn
        self.current_dir = current_dir


    def task(self,user_dict,q):
        while True:
            try:
                cmd = self.conn.recv(1024)
                print(cmd)
                if not cmd: break
                cmd_list = cmd.decode(self.coding).split()
                cmd_list.append(user_dict['username'])
                if hasattr(self, cmd_list[0]):
                    func = getattr(self, cmd_list[0])
                    func(cmd_list)
            except ConnectionResetError:
                q.get()
                break
        self.conn.close()


    def get(self,cmd_list):        #下载
        filename = cmd_list[1]
        file_list = os.listdir( self.current_dir)
        for i in file_list:
            if not os.path.isfile(os.path.join( self.current_dir, i)):
                file_list.pop(file_list.index(i))
        if filename not in file_list:
            header_dict = {
                'filename': filename,
                'file_list': file_list,
            }  # 生成报头
            header_json = json.dumps(header_dict)  # 将报头转成字符串
            header_bytes = header_json.encode('utf-8')  # 将报头转成字节
            self.conn.send(struct.pack('i', len(header_bytes)))
            self.conn.send(header_bytes)
            self.conn.send('file not exists'.encode(self.coding))
            return
        header_dict = {
            'username':cmd_list[2],
            'total_size':os.path.getsize('{}\{}'.format( self.current_dir,filename)),
            'filename':filename,
            'md5':self._get_md5('{}\{}'.format( self.current_dir,filename)),
            'file_list':file_list,
        }    #生成报头
        header_json = json.dumps(header_dict)                     #将报头转成字符串
        header_bytes = header_json.encode('utf-8')              #将报头转成字节
        self.conn.send(struct.pack('i',len(header_bytes)))
        self.conn.send(header_bytes)
        with open('{}\{}'.format( self.current_dir,filename),'rb') as f:
            for i in f:
                self.conn.send(i)
        logger.logger('{} get file {} successful'.format(cmd_list[2],filename))


    def put(self,cmd_list):        #上传
        filename = cmd_list[1]
        self.conn.send(b'ok')
        obj = self.conn.recv(4)
        header_size = struct.unpack('i', obj)[0]  # 获取报头长度
        header_bytes = self.conn.recv(header_size)  # 报头字节
        header_json = header_bytes.decode('utf-8')  # 报头字符串
        header_dict = json.loads(header_json)  # 报头字典
        total_size = header_dict['total_size']  # 数据总长度
        filename = header_dict['filename']
        config = RUN._get_config()
        quota_size = int(config[cmd_list[2]]['quota'])*1024*1024
        root_dir = os.path.join(os.path.join(settings.BASE_DIR, 'share'), str(config[cmd_list[2]]['home_dir']))
        current_home_size = self._get_dir_size(root_dir)
        if current_home_size + total_size < quota_size:
            self.conn.send('ok'.encode(self.coding))
            with open('{}\{}'.format( self.current_dir, filename), 'wb') as f:
                # print(total_size)
                recv_size = 0
                while recv_size < total_size:  # 循环获取数据，直到完成
                    res = self.conn.recv(1024)
                    f.write(res)
                    recv_size += len(res)
                    # print('总大小：{}   已下载：{}'.format(total_size, recv_size))
            new_file_md5 = self._get_md5('{}\{}'.format( self.current_dir, filename))
            if new_file_md5 == header_dict['md5']:
                self.conn.send(new_file_md5.encode(self.coding))
                logger.logger('{} put file {} successful'.format(cmd_list[2], filename))
            else:
                self.conn.send('not'.encode(self.coding))
        else:self.conn.send('not'.encode(self.coding))


    def _get_md5(self,filename):        #获取文件的md5值
        m = hashlib.md5()
        with open(filename,'rb') as f:
            m.update(f.read())
        return m.hexdigest()


    def dir(self,cmd_list):    #用户查看当前目录下文件
        if cmd_list[1] == '.':
            dir_name =  self.current_dir
        else:
            dir_name = os.path.join( self.current_dir,cmd_list[1])
        obj = subprocess.Popen('dir {}'.format(dir_name),
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        stdout = obj.stdout.read()
        stderr = obj.stderr.read()
        # print(len(stdout)+len(stderr))
        header_dict = {'total_size': len(stdout) + len(stderr)}  # 生成报头
        header_json = json.dumps(header_dict)  # 将报头转成字符串
        header_bytes = header_json.encode(self.coding)  # 将报头转成字节
        self.conn.send(struct.pack('i', len(header_bytes)))
        self.conn.send(header_bytes)
        self.conn.send(stdout)
        self.conn.send(stderr)


    def cd(self,cmd_list):     #切换目录
        config = RUN._get_config()
        root_dir = os.path.join(os.path.join(settings.BASE_DIR, 'share'), str(config[cmd_list[2]]['home_dir']))
        if cmd_list[1] == '.':
            self.current_dir = root_dir
        elif cmd_list[1] == '..':
            if root_dir ==  self.current_dir:
                self.current_dir = root_dir
            else:
                self.current_dir = os.path.dirname( self.current_dir)


        else:
            self.current_dir = os.path.join( self.current_dir, cmd_list[1])
            if not os.path.isdir( self.current_dir):
                self.conn.send('not'.encode(self.coding))
                self.current_dir = os.path.dirname( self.current_dir)
                return
            else:
                self.current_dir= self.current_dir
        self.conn.send( self.current_dir.split('share')[1].encode(self.coding))


    def pwd(self,cmd_list):        #获取当前路径
        header_dict = {'total_size': len( self.current_dir.encode(self.coding)),
                       'username':cmd_list[1]
                       }  # 生成报头
        header_json = json.dumps(header_dict)  # 将报头转成字符串
        header_bytes = header_json.encode(self.coding)  # 将报头转成字节
        self.conn.send(struct.pack('i', len(header_bytes)))
        self.conn.send(header_bytes)
        self.conn.send( self.current_dir.encode(self.coding))


    def _get_dir_size(self,dir):    #获取文件夹大小
        size = 0
        for root, dirs, files in os.walk(dir):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return size





# server.close()