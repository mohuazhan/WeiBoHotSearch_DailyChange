# -*- coding: utf-8 -*-

import datetime


def original_dates():
    start='2019-08-01'
    end='2019-08-05'

    datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
    dateend=datetime.datetime.strptime(end,'%Y-%m-%d')

    date_list = list()
    while datestart<=dateend:
        date_list.append(datestart.strftime('%Y/%m/%d')) 
        datestart+=datetime.timedelta(days=1)

    return date_list
