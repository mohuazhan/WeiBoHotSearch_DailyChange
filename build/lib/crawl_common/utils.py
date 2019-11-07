# -*- coding: utf-8 -*-

import datetime


# 手动获取时间列表
def original_dates():
    start='2019-09-06'
    end='2019-11-06'

    datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
    dateend=datetime.datetime.strptime(end,'%Y-%m-%d')

    date_list = list()
    while datestart<=dateend:
        date_list.append(datestart.strftime('%Y/%m/%d')) 
        datestart+=datetime.timedelta(days=1)

    return date_list


# 为TDengine构造ts值
def new_ts(date):
    time_now = datetime.datetime.now().strftime('%H:%M:%S.%f')[0:12]  # 从小时取到毫秒
    new_ts = date + ' ' + time_now
    return new_ts
