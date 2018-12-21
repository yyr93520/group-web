# -*- coding: utf-8 -*-

import time
import config

class Session(object):

    @staticmethod
    def timeReduction(sms_list):
        timestamp = []
        for sms in sms_list:
            timestamp.append(time.mktime(time.strptime(sms['time'], "%Y-%m-%d %H:%M:%S")))
        tag_list = Session.splitTime(timestamp)
        return tag_list

    @staticmethod
    def splitTime(timestamp):
        dur_time_rate = config.DURING_RATE
        dur_time_thresh = config.DURING_THRESHOLD
        tag_list = []
        during = [timestamp[i + 1] - timestamp[i] for i in range(len(timestamp) - 1)]
        during_sort = sorted(during, reverse=True)
        acc_num = len(during) * (1 - dur_time_rate)
        add_num = 0
        split_time = 0
        for dur in during_sort:
            add_num += 1
            if add_num > acc_num:
                split_time = dur
                break
        tag_list.append(1)
        for dur in during:
            if dur > split_time or dur >= dur_time_thresh:
                tag_list[-1] = 2
                tag_list.append(1)
            else:
                tag_list.append(0)
        if tag_list[-1] != 1:
            tag_list[-1] = 2
        return tag_list

if __name__ == '__main__':
    model = Session()
    #model.timeReduction()
    model.splitTime([1533617220.0, 1533617280.0])

