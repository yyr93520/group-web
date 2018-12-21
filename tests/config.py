# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))
idcarddir = os.path.join(basedir, 'idcard.txt')
inputdir = os.path.join(basedir, 'input/')
outputdir = os.path.join(basedir, 'output/')

location_list = ['天安门', '中南海', '国家信访局', '退役军人事务部', '军委信访处', '八一大楼']

location_dict = {
    '天安门' : (116.403847,39.915526),
    '中南海' : (116.390628,39.921297),
    '国家信访局' : (116.357596,39.919134),
    '退役军人事务部' : (116.425826,40.041765),
    #'军委信访处' : (),
    '八一大楼' : (116.33369,39.915313)
}

