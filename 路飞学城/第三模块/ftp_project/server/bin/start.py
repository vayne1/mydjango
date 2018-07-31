#!_*_coding:utf-8_*_

import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(base_dir)

from core import socket_server
from conf import settings


if __name__ == '__main__':
    server = socket_server.FTP_server((settings.IP_ADDRESS, settings.PORT))
    server.run()


