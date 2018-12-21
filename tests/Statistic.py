# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import config
import xlwt
import util
import time

class Statistic(object):

    def __init__(self):
        self.book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.file_list = util.get_days_before_today()
        self.phone2id = util.phone_id_dict()
        self.keyperson = []
        self.keyperson_info = {}
        self.id2phone = {}
        self.location_dict = {}

    def execute(self):
        self.inBeijing()
        self.keyPersonInfo()
        self.getLocationDict()
        self.keyArea()
        self.keyPersonGather()
        self.frequentArea()
        self.movingTrack()
        self.writeExcel()

    def inBeijing(self):
        sheet = self.book.add_sheet('长期在京或频繁进京人员', cell_overwrite_ok=True)
        sheet.write(0, 0,'身份证号码'.decode('utf-8'), util.def_style())
        sheet.write(0, 1, '手机号码'.decode('utf-8'), util.def_style())
        sheet.write(0, 2, '人员类型'.decode('utf-8'), util.def_style())
        user2day = {}
        for file in self.file_list:
            with open(file, 'r') as fin:
                for line in fin.readlines():
                    info_list = line.strip().split('\t')
                    phone = info_list[0]
                    user = self.phone2id[phone]
                    if not self.id2phone.has_key(user):
                        self.id2phone[user] = set()
                    self.id2phone[user].add(phone)
                    province = info_list[1]
                    if province != "北京市":
                        continue
                    time = info_list[7]
                    if not user2day.has_key(user):
                        user2day[user] = set()
                    user_set = user2day[user]
                    day = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").day
                    user_set.add(day)
        idx = 1
        for user in user2day:
            day_len = len(user2day[user])
            sheet.write(idx, 0, user)
            sheet.write(idx, 1, ','.join(self.id2phone[user]))
            if day_len >= 20:
                sheet.write(idx, 2, '长期在京'.decode('utf-8'), util.def_style())
                self.keyperson.append(user)
            if day_len >= 10 and day_len < 20:
                sheet.write(idx, 2, '频繁进京'.decode('utf-8'), util.def_style())
                self.keyperson.append(user)
            idx += 1

    def keyPersonInfo(self):
        for file in self.file_list:
            with open(file, 'r') as fin:
                for line in fin.readlines():
                    info_list = line.strip().split('\t')
                    phone = info_list[0]
                    user = self.phone2id[phone]
                    province = info_list[1]
                    if user not in self.keyperson:
                        continue
                    lon = info_list[5]
                    lat = info_list[6]
                    time = info_list[7]
                    location = info_list[4]
                    if not self.keyperson_info.has_key(user):
                        self.keyperson_info[user] = []
                    self.keyperson_info[user].append([phone, lon, lat, time, location, province])
        for user in self.keyperson_info:
            self.keyperson_info[user] = sorted(self.keyperson_info[user], key = lambda info : info[3])

    def keyArea(self):
        sheet = self.book.add_sheet('重点区域的重点人', cell_overwrite_ok=True)
        sheet.write(0, 0, '身份证号码'.decode('utf-8'))
        sheet.write(0, 1, '手机号码'.decode('utf-8'))
        sheet.write(0, 2, '重点区域'.decode('utf-8'))
        sheet.write(0, 3, '频次'.decode('utf-8'))
        sheet.write(0, 4, '停留时长(h)'.decode('utf-8'))
        keyarea_list = config.location_list
        index = 1
        for user in self.keyperson_info:
            info_list = self.keyperson_info[user]
            area_dict = {}
            for idx in range(len(info_list)):
                info = info_list[idx]
                phone = info[0]
                loc = info[4]
                start_time = datetime.strptime(info[3], "%Y-%m-%d %H:%M:%S")
                for keyarea in keyarea_list:
                    if not keyarea in loc:
                        continue
                    if not area_dict.has_key(keyarea):
                        area_dict[keyarea] = {'phone' : set(), 'frequence' : set(), 'duration' : 0}
                    area_dict[keyarea]['phone'].add(phone)
                    area_dict[keyarea]['frequence'].add(start_time.day)
                    if idx + 1 < len(info_list):
                        end_time = datetime.strptime(info_list[idx + 1][3], "%Y-%m-%d %H:%M:%S")
                        duration = (end_time - start_time).total_seconds()
                        area_dict[keyarea]['duration'] += duration
                    else:
                        area_dict[keyarea]['duration'] += 3600

            for area in area_dict:
                sheet.write(index, 0, user)
                sheet.write(index, 1, ','.join(area_dict[area]['phone']))
                sheet.write(index, 2, area)
                sheet.write(index, 3, len(area_dict[area]['frequence']))
                sheet.write(index, 4, round(area_dict[area]['duration'] / 3600))
                index += 1

    def getLocationDict(self):
        self.location_dict = {}
        for user in self.keyperson_info:
            info_list = self.keyperson_info[user]
            idx = 0
            while idx < len(info_list):
                info = info_list[idx]
                if info[5] != '北京市':
                    idx += 1
                    continue
                loc = info[4]
                if not self.location_dict.has_key(info[4]):
                    self.location_dict[info[4]] = dict()
                if not self.location_dict[info[4]].has_key(user):
                    self.location_dict[info[4]][user] = set()
                start_time = datetime.strptime(info[3], "%Y-%m-%d %H:%M:%S")
                time_tag = datetime(start_time.year, start_time.month, start_time.day, start_time.hour)
                while idx < len(info_list) and info_list[idx][4] == loc:
                    idx += 1
                if idx < len(info_list):
                    end_time = datetime.strptime(info_list[idx][3], "%Y-%m-%d %H:%M:%S")
                    duration = (end_time - start_time).total_seconds() / 3600
                else:
                    end_time = datetime.strptime(info_list[idx - 1][3], "%Y-%m-%d %H:%M:%S")
                    duration = (end_time - start_time).total_seconds() / 3600 + 1
                self.location_dict[info[4]][user].add((time_tag, duration))

    def keyPersonGather(self):
        index = 0
        sheet = self.book.add_sheet('重点人聚团情况', cell_overwrite_ok=True)
        sheet.write_merge(index, index, 0, 3, '3小时内在同一地点出现'.decode('utf-8'), util.def_style())
        index += 1
        sheet.write(index, 0, '停留地点'.decode('utf-8'), util.def_style())
        sheet.write(index, 1, '重点人'.decode('utf-8'), util.def_style())
        sheet.write(index, 2, '电话号码'.decode('utf-8'), util.def_style())
        sheet.write(index, 3, '停留时间'.decode('utf-8'), util.def_style())
        index += 1
        time_list = util.get_hours_before_today()
        for start_time in time_list:
            end_time = start_time + timedelta(hours = 3)
            for location in self.location_dict:
                user_set = set()
                phone_list = list()
                for user in self.location_dict[location]:
                    for info_pair in self.location_dict[location][user]:
                        if info_pair[0] >= end_time:
                            continue
                        if info_pair[0] + timedelta(hours = info_pair[1]) < start_time:
                            continue
                        user_set.add(user)
                        phone_list += self.id2phone[user]
                        break
                if len(user_set) < 2:
                    continue
                time_str = start_time.strftime("%Y-%m-%d %H:%M:%S") + '——' + end_time.strftime("%Y-%m-%d %H:%M:%S")
                sheet.write(index, 0, location.decode('utf-8'))
                sheet.write(index, 1, ','.join(user_set))
                sheet.write(index, 2, ','.join(phone_list))
                sheet.write(index, 3, time_str)
                index += 1

        sheet.write_merge(index, index, 0, 3, '同一地点3人以上停留时间重合'.decode('utf-8'), util.def_style())
        index += 1
        sheet.write(index, 0, '停留地点'.decode('utf-8'), util.def_style())
        sheet.write(index, 1, '重点人'.decode('utf-8'), util.def_style())
        sheet.write(index, 2, '电话号码'.decode('utf-8'), util.def_style())
        sheet.write(index, 3, '停留时长(h)'.decode('utf-8'), util.def_style())
        index += 1
        for location in self.location_dict:
            user_set = set()
            user_list = self.location_dict[location].keys()
            for i in range(len(user_list)):
                cover_list = []
                user_a = user_list[i]
                if user_a in user_set:
                    continue
                user_set.add(user_a)
                cover_list.append(user_a)
                for j in range(i + 1, len(user_list)):
                    user_b = user_list[j]
                    if user_b in user_set:
                        continue
                    if len(self.location_dict[location][user_a] - self.location_dict[location][user_b]) != 0:
                        continue
                    user_set.add(user_b)
                    cover_list.append(user_b)
                if len(cover_list) < 3:
                    continue
                duration = 0
                for pair in self.location_dict[location][user_a]:
                    duration += pair[1]
                phone_list = []
                for user in cover_list:
                    phone_list += list(self.id2phone[user])
                sheet.write(index, 0, location.decode('utf-8'), util.def_style())
                sheet.write(index, 1, ",".join(cover_list), util.def_style())
                sheet.write(index, 2, ",".join(phone_list), util.def_style())
                sheet.write(index, 3, duration, util.def_style())
                index += 1

    def frequentArea(self):
        index = 0
        sheet = self.book.add_sheet('出现频次高的地区', cell_overwrite_ok=True)
        sheet.write(index, 0, '停留地点'.decode('utf-8'), util.def_style())
        sheet.write(index, 1, '重点人数目'.decode('utf-8'), util.def_style())
        sheet.write(index, 2, '总频次'.decode('utf-8'), util.def_style())
        sheet.write(index, 3, '单人最高频次'.decode('utf-8'), util.def_style())
        index += 1
        for location in self.location_dict:
            user_num = len(self.location_dict[location])
            freq_sum = 0
            freq_max = 0
            for user in self.location_dict[location]:
                freq = len(self.location_dict[location][user])
                freq_max = max(freq, freq_max)
                freq_sum += freq
            if user_num < 2 and freq_max < 2:
                continue
            sheet.write(index, 0, location.decode('utf-8'))
            sheet.write(index, 1, user_num)
            sheet.write(index, 2, freq_sum)
            sheet.write(index, 3, freq_max)
            index += 1

    def movingTrack(self):
        index = 0
        sheet = self.book.add_sheet('移动轨迹相同的同行人', cell_overwrite_ok=True)
        sheet.write(index, 0, '同行人'.decode('utf-8'), util.def_style())
        sheet.write(index, 1, '电话号码'.decode('utf-8'), util.def_style())
        index += 1
        user_dict = {}
        for location in self.location_dict:
            for user in self.location_dict[location]:
                if not user_dict.has_key(user):
                    user_dict[user] = set()
                for time_pair in self.location_dict[location][user]:
                    user_dict[user].add((location, time_pair[0], time_pair[1]))
        user_set = set()
        user_list = user_dict.keys()
        for i in range(len(user_list)):
            cover_set = set()
            user_a = user_list[i]
            if user_a in user_set:
                continue
            user_set.add(user_a)
            cover_set.add(user_a)
            for j in range(i + 1, len(user_list)):
                user_b = user_list[j]
                if user_b in user_set:
                    continue
                if len(user_dict[user_a] - user_dict[user_b]) != 0:
                    continue
                user_set.add(user_b)
                cover_set.add(user_b)
            if len(cover_set) < 2:
                continue
            phone_list = []
            for user in cover_set:
                phone_list += list(self.id2phone[user])
            sheet.write(index, 0, ",".join(cover_set), util.def_style())
            sheet.write(index, 1, ",".join(phone_list), util.def_style())
            index += 1


    def writeExcel(self):
        outputdir = config.outputdir
        filename = time.strftime("%Y-%m-%d") + '.xls'
        outputfile = os.path.join(outputdir, filename)
        self.book.save(outputfile)

if __name__=='__main__':
    obj = Statistic()
    obj.execute()