#!_*_coding:utf-8_*_

import os
import sys
import logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER_FILE = '{}/db/user_info'.format(BASE_DIR)

COURSE_FILE = '{}/db/course_info'.format(BASE_DIR)

SCHOOL_FILE = '{}/db/school_info'.format(BASE_DIR)

GRADE_FILE = '{}/db/grade_info'.format(BASE_DIR)

LOG_FILE = '{}/log/access.log'.format(BASE_DIR)

