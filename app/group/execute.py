# -*- coding: utf-8 -*-

from app import mongo, util
import config
import json
from groupOp import GroupOp
import time

class Execute(object):

    def __init__(self):
        self.loc_encode = util.province_encode()

    def execute(self, group_name, keyword, start_time, end_time, location, seeduser):
        self.group_name = group_name
        self.keyword = keyword
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.seed_user = seeduser
        group_id = GroupOp.createGroup(self.group_name, self.keyword, self.start_time, self.end_time, self.location)
        sms_list = GroupOp.searchSms(self.keyword, self.start_time, self.end_time, self.location, self.seed_user)
        session_list = set()
        for sms in sms_list:
            session_list.add(sms['session_id'])
        self.locDistribution(group_id, session_list)
        self.sessionReduction(group_id, session_list)
        return group_id

    def abstract(self, group_id, session_list):
        pass

    def sessionReduction(self, group_id, session_list):
        keyword_list = self.keyword.strip().split(" ")
        sms_info = []
        idx = 0
        for session_id in session_list:
            session_record = mongo.db['session'].find_one({'session_id': session_id})
            sms_id_list = session_record['sms_id_list']
            sms_show = dict()
            keyword_set = set()
            sms_list = list()
            user_pos = dict()
            for sms_id in sms_id_list:
                sms = mongo.db['sms'].find_one({'sms_id': sms_id})
                keywords = sms['keywords']
                overlap = set([val for val in keywords if val in keyword_list])
                keyword_set = keyword_set | overlap
                if len(user_pos) == 0:
                    user_pos[sms['sender']] = 'left'
                    user_pos[sms['receiver']] = 'right'
                sms_list.append({'sender':sms['sender'], 'sms':sms['sms'], 'pos':user_pos[sms['sender']], 'time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sms['time']))})
                if len(sms_show) == 0 and len(keyword_set) > 0:
                    sms_show = sms
            if len(sms_show) == 0:
                continue
            sms_show['rate'] = len(keyword_set) * 1.0 / (len(keyword_list) + 1)
            sms_show['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sms_show['time']))
            sms_show['sms_list'] = sms_list
            sms_show['index'] = idx
            idx += 1
            sms_info.append(sms_show)
        show_num = config.SMS_SHOW_NUM
        sms_info = sorted(sms_info, key=lambda sms : sms['rate'])[:show_num]
        session_result = {'group_id':group_id, 'sms_info':sms_info}
        print session_result
        mongo.db['reduction'].insert(session_result)
        return

    def locDistribution(self, group_id, session_list):
        sms_id_list = []
        for session_id in session_list:
            session_record = mongo.db['session'].find_one({'session_id': session_id})
            sms_id_list += session_record['sms_id_list']
        loc_dict = {}
        loc_pair_dict = {}
        for sms_id in sms_id_list:
            sms = mongo.db['sms'].find_one({'sms_id':sms_id})
            senderdqs = self.loc_encode[sms['senderdqs']]
            receiverdqs = self.loc_encode[sms['receiverdqs']]
            if not loc_dict.has_key(senderdqs):
                loc_dict[senderdqs] = 0
            if not loc_dict.has_key(receiverdqs):
                loc_dict[receiverdqs] = 0
            if not loc_pair_dict.has_key(senderdqs + '@' + receiverdqs):
                loc_pair_dict[senderdqs + '@' + receiverdqs] = 0
            loc_dict[senderdqs] += 1
            loc_dict[receiverdqs] += 1
            loc_pair_dict[senderdqs + '@' + receiverdqs] += 1
        node_json = []
        for loc in loc_dict:
            node_json.append(json.dumps({'name':loc,'value':loc_dict[loc]}))
        edge_json = []
        for loc_pair in loc_pair_dict:
            pair = loc_pair.split('@')
            edge_json.append([json.dumps({'name':pair[0]}), json.dumps({'name':pair[1],'value':loc_pair_dict[loc_pair]})])
        loc_result = {'group_id':group_id, 'node_json':node_json, 'edge_json':edge_json}
        mongo.db['location'].insert(loc_result)
        return
