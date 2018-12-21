# -*- coding: utf-8 -*-

from app import mongo, util
import config
import os
import time

class GroupOp(object):

    def __init__(self):
        pass

    @staticmethod
    def createGroup(group_name, keyword, start_time, end_time, location):
        group_id = mongo.db['colony'].find().count() + 2
        start_time = start_time.timetuple()
        end_time = end_time.timetuple()
        group_json = {'group_id' : group_id, 'group_name': group_name, 'keyword': keyword, 'start_time': time.mktime(start_time), 'end_time': time.mktime(end_time),
                      'location': location}
        mongo.db['colony'].insert(group_json)
        return group_id

    @staticmethod
    def searchSms(keyword, start_time, end_time, location, seed_user):
        start_time = time.mktime(start_time.timetuple())
        end_time = time.mktime(end_time.timetuple())
        if location == '0':
            sms_cursor = mongo.db['sms'].find({"time":{"$gte":start_time, "$lte":end_time}, "$text":{"$search":keyword}})
        else:
            sms_cursor = mongo.db['sms'].find(
                {"time": {"$gte": start_time, "$lte": end_time}, "$or":[{"senderdqs":location},{"receiverdqs":location}], "$text": {"$search": keyword}})
        sms_list = list(sms_cursor)
        if seed_user != '':
            seed_fp = os.path.join(config.UPLOAD_FOLDER, seed_user)
            users = list()
            with open(seed_fp, 'r') as fin:
                for line in fin.readlines():
                    users.append(line.strip())
            sms_cursor = mongo.db['sms'].find({"$or":[{"sender":{"$in":users}},{"receiver":{"$in":users}}]})
            sms_list += list(sms_cursor)
        sms_set = []
        for item in sms_list:
            if not item in sms_set:
                sms_set.append(item)
        return sms_set

    @staticmethod
    def getGroupList():
        group_list = list()
        group_cursor = mongo.db['colony'].find()
        prov_encode = util.province_encode()
        for group in group_cursor:
            group['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(group['start_time']))
            group['end_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(group['end_time']))
            group['location'] = prov_encode[group['location']]
            group_list.append(group)

        return list(group_list)

    @staticmethod
    def getLocation(group_id):
        for i in range(5):
            loc_result = mongo.db['location'].find_one({'group_id':group_id})
            if loc_result != None:
                return loc_result['node_json'], loc_result['edge_json']
            time.sleep(1)
        return {}, {}

    @staticmethod
    def getSMSList(group_id):
        for i in range(5):
            sms_info = mongo.db['reduction'].find_one({'group_id':group_id})
            if sms_info != None:
                return sms_info['sms_info']
            time.sleep(1)
        return {}