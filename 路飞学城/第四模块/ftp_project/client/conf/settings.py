# -*- coding:utf-8 -*-

import os
import sys
import logging

IP_ADDRESS = '127.0.0.1'

PORT = 9999

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOWNLOAD_DIR = os.path.join(BASE_DIR,'download')

LOG_FILE = os.path.join(os.path.join(BASE_DIR,'log'),'access.log')