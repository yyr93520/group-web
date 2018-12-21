# -*- coding: utf-8 -*-

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

import os
basedir = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(basedir, 'data')
stopword = os.path.join(basedir, 'stopword.txt')

TIMEINTERVAL = 3600
DURING_RATE = 0.9
DURING_THRESHOLD = 43200
SENDER_ID = 3
RECEIVER_ID = 4
TIME = 2
SMS = 5
POINT2POINT = 6
SENDERSSD = 5
SENDERSSQH = 6
SENDERDQS = 0
SENDERDQQH = 8
RECEIVERSSD = 9
RECEIVERSSQH = 10
RECEIVERDQS = 1
RECEIVERDQQH = 12