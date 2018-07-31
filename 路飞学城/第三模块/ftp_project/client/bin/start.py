#!_*_coding:utf-8_*_

import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from core import socket_client
from conf import settings


if __name__ == '__main__':
    client = socket_client.FTP_client((settings.IP_ADDRESS, settings.PORT))
    client.run()


