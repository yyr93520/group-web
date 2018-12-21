# -*- coding:utf-8 -*-

from MongodbClient import MongodbClient
import os
import jieba.posseg as pseg
from session import Session
import uuid
import config
import time
import json

class Hive2Mongo(object):
    def __init__(self, filefolder):
        self.filefolder = filefolder
        self.mongodbClient = MongodbClient('localhost', 27017, 'group', 'smstest')
        self.id2session = self.sessionReduction()
        self.stop = [line.strip() for line in open(config.stopword, 'r').readlines()]
        self.session2id = dict()

    def sessionReduction(self):
        filepath = os.path.join(os.getcwd(),self.filefolder)
        pathDir = os.listdir(filepath)
        pair2id = {}
        pair_dict = {}
        id2session = {}
        idx = 0
        sms_id = -1
        session_max = list(self.mongodbClient.db['sessiontest'].find().sort([("session_id",-1)]).limit(1))
        if session_max == []:
            session_id = 0
        else:
            session_id = session_max[0]['session_id']
        for allDir in pathDir:
            child = os.path.join('%s/%s' % (filepath, allDir))
            if os.path.isfile(child):
                with open(child, 'r') as fin:
                    for line in fin.readlines():
                        sms_id += 1
                        info_list = line.strip().split('\t')
                        if cmp(info_list[config.SENDER_ID], info_list[config.RECEIVER_ID]) < 0:
                            user = info_list[config.SENDER_ID] + '@' + info_list[config.RECEIVER_ID]
                        else:
                            user = info_list[config.RECEIVER_ID] + '@' + info_list[config.SENDER_ID]
                        if not pair2id.has_key(user):
                            pair2id[user] = idx
                            idx += 1
                        user_id = pair2id[user]
                        if not pair_dict.has_key(user_id):
                            pair_dict[user_id] = []
                        user_sms = {}
                        user_sms['time'] = info_list[config.TIME]
                        user_sms['id'] = sms_id
                        pair_dict[user_id].append(user_sms)
        for id in pair_dict:
            users_sms = sorted(pair_dict[id], key=lambda x: time.mktime(time.strptime(x['time'], "%Y-%m-%d %H:%M:%S")))
            tag_list = Session.timeReduction(users_sms)
            for i in range(len(tag_list)):
                if tag_list[i] == 1:
                    session_id += 1
                id2session[users_sms[i]['id']] = session_id
        return id2session

    def importSMS(self):
        filepath = os.path.join(os.getcwd(), self.filefolder)
        pathDir = os.listdir(filepath)
        sms_id = -1
        sms_list = list()
        sms_set = set()
        sms_max = list(self.mongodbClient.db['smstest'].find().sort([("sms_id",-1)]).limit(1))
        if len(sms_max) == 0:
            sms_db_id = 0
        else:
            sms_db_id = sms_max[0]['sms_id']
        for allDir in pathDir:
            child = os.path.join('%s/%s' % (filepath, allDir))
            if os.path.isfile(child):
                with open(child, 'r') as fin:
                    for line in fin.readlines():
                        line = line.strip()
                        sms_id += 1
                        info_list = line.split('\t')
                        if "未来管家" in info_list[config.SMS] or "请回电话" in info_list[config.SMS] or "中国移动" in info_list[
                            config.SMS]:
                            continue
                            ''' 测试用  中心取消注释
                        if not len(info_list[config.SENDER_ID]) in [11, 13] or not len(
                                info_list[config.RECEIVER_ID]) in [11, 13]:
                            continue
                            '''
                        if info_list[config.POINT2POINT] != "1":
                            continue
                        if line in sms_set:
                            continue
                        sms_set.add(line)
                        sms = dict()
                        keywords = pseg.cut(info_list[config.SMS])
                        keywords = [word.word.strip().encode('utf-8') for word in keywords if word.flag[0] != 'x']
                        keywords = [word for word in keywords if word not in self.stop]
                        sms_db_id += 1
                        sms['sender'] = info_list[config.SENDER_ID]
                        sms['receiver'] = info_list[config.RECEIVER_ID]
                        sms['time'] = time.mktime(time.strptime(info_list[config.TIME], "%Y-%m-%d %H:%M:%S"))
                        sms['sms'] = info_list[config.SMS]
                        sms['keywords'] = keywords
                        sms['senderdqs'] = info_list[config.SENDERDQS]
                        sms['receiverdqs'] = info_list[config.RECEIVERDQS]
                        sms['sms_id'] = sms_db_id

                        ''' 测试用 中心取消注释
                        sms['senderssd'] = info_list[config.SENDERSSD]
                        sms['senderssqh'] = info_list[config.SENDERSSQH]
                        sms['senderdqqh'] = info_list[config.SENDERDQQH]
                        sms['receiverssd'] = info_list[config.RECEIVERSSD]
                        sms['receiverssqh'] = info_list[config.RECEIVERSSQH]
                        sms['receiverdqqh'] = info_list[config.RECEIVERDQQH]
                        '''
                        session_id = self.id2session[sms_id]
                        sms['session_id'] = session_id
                        if not self.session2id.has_key(session_id):
                            self.session2id[session_id] = list()
                        self.session2id[session_id].append(sms_db_id)
                        sms_list.append(sms)
                        if len(sms_list) >= 100:
                            self.mongodbClient.put_many(sms_list)
                            sms_list = list()
                            sms_set = set()
                    self.mongodbClient.put_many(sms_list)

    def importSession(self):
        session_list = []
        for session_id in self.session2id:
            session_list.append({'session_id':session_id, 'sms_id_list':self.session2id[session_id]})
        self.mongodbClient.changeTable('sessiontest')
        self.mongodbClient.put_many(session_list)


if __name__ == "__main__":
    hive2mongo = Hive2Mongo('data')
    hive2mongo.importSMS()
    hive2mongo.importSession()