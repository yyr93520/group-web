# -*- coding: utf-8 -*-
import config

def loc_list():
    loc = []
    with open(config.provincedir, 'r') as fin:
        for line in fin.readlines():
            info_list = line.strip().split(' ')
            loc.append((info_list[0], info_list[1]))
    return loc


def province_encode():
    loc_encode = {}
    with open(config.provincedir, 'r') as fin:
        for line in fin.readlines():
            line = line.strip().split(' ')
            loc_encode[line[0]] = line[1]
    return loc_encode

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS