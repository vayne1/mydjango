#!_*_coding:utf-8_*_

import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(base_dir)

from core import socket_server
from conf import settings


if __name__ == '__main__':
    server = socket_server.RUN((settings.IP_ADDRESS, settings.PORT,),3)  #3为最大并发数
    server.run()


