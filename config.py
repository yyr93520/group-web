# -*- coding: utf-8 -*-
import os
from datetime import timedelta

CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)

basedir = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(basedir, 'data')
provincedir = os.path.join(datadir, 'province.txt')
UPLOAD_FOLDER = os.path.join(basedir, 'app/static/upload')

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'group'
MONGO_TABLE = 'sms'
MONGO_USERNAME = 'admin'
MONGO_PASSWORD = '123456'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

TIMEINTERVAL = 3600
DURING_RATE = 0.9
DURING_THRESHOLD = 43200
SMS_SHOW_NUM = 100