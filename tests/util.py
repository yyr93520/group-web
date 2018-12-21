# -*- coding: utf-8 -*-
import math
import sys
import config
import datetime
import os
import xlwt

def get_days_before_today(n=30):
    days_list = []
    now = datetime.datetime.now()
    file_list = []
    for i in range(n, 0, -1):
        n_days_before = now - datetime.timedelta(days=i)
        day_date = datetime.date(n_days_before.year, n_days_before.month, n_days_before.day)
        days_list.append(day_date.strftime("%Y-%m-%d"))
    hour_list = ['4', '16']
    for day in days_list:
        for hour in hour_list:
            file_name = day + '_' + hour + '.txt'
            file_path = os.path.join(config.inputdir, file_name)
            if os.path.exists(file_path):
                file_list.append(file_path)
    return file_list

def get_hours_before_today(n = 30):
    time_list = []
    now = datetime.datetime.now()
    before = now - datetime.timedelta(days=n)
    day_date = datetime.datetime(before.year, before.month, before.day)
    for i in range(0, 720, 3):
        time_list.append(day_date + datetime.timedelta(hours = i))
    return time_list

def lat_lon_var(dis=1):
    cons = 111.
    loc_dict = config.location_dict
    keyarea_list = []
    for loc in loc_dict:
        lon = loc_dict[loc][0]
        lat = loc_dict[loc][1]
        lat_var = 1./cons*dis
        lon_var = 1./cons/math.radians(lat)*dis
        keyarea = {'name' : loc, 'lon_range' : (lon-lon_var, lon_var+lon), 'lat_range' : (lat-lat_var, lat_var+lat)}
        keyarea_list.append(keyarea)
    return keyarea_list

def compare_loc(lon, lon_range, lat, lat_range):
    if lon >= lon_range[0] and lon <= lon_range[1] and lat >= lat_range[0] and lat <= lat_range[1]:
        return True
    else:
        return False

def phone_id_dict():
    phone2id = {}
    with open(config.idcarddir, 'r') as fin:
        for line in fin.readlines():
            info_list = line.strip().split('\t')
            phone2id[info_list[1]] = info_list[0]
    return phone2id


def def_style():
    style = xlwt.XFStyle()
    font = xlwt.Font()
    #font.name = 'Times New Roman'  # 或者换成外面传进来的参数，这样可以使一个函数定义所有style
    #font.bold = 'True'
    #font.height = '...'
    font.size = '12'
    #font.colour_index('...')
    style.font = font
########这部分设置居中格式#######
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直居中
    style.alignment = alignment

#########还可以添加几个设置颜色，边框的部分##########

    return style

if __name__=='__main__':
    '''
	if len(sys.argv)<4:
		print('please input [latitude,longtitude,distance(km)]')
		sys.exit(1)
	lon = float(sys.argv[1])
	lat = float(sys.argv[2])
	dis = float(sys.argv[3])
	lat_var, lon_var = lat_lon_var(lat, lon, dis)
	print([(lon_var+lon, lat_var+lat),(lon-lon_var, lat-lat_var)])
    '''
    print get_hours_before_today()