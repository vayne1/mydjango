#!_*_coding:utf-8_*_

import logging
from conf import settings


def logger(msg):
    logging.basicConfig(filename=settings.LOG_FILE,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.warning(msg)