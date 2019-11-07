# -*- coding: utf-8 -*-

import json
import logging
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import tornado.gen
from tornado.concurrent import run_on_executor

from utils import param_md5
from consts import HOTSEARCH_WEIBO_URL, RESPONSE_CODE
from handlers.common import CommonHandler

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logger = logging.getLogger(__name__)


class WeiboHotsearchHandler(CommonHandler):
    '''
    处理微博热搜请求(/v1/spider/hotsearch/weibo)的Handler
    handle_args：校验传入参数
    '''

    def __init__(self, *args, **kwargs):
        super(WeiboHotsearchHandler, self).__init__(*args, **kwargs)

    def initialize(self, *args, **kwargs):
        super(WeiboHotsearchHandler, self).initialize(*args, **kwargs)

    def handle_args(self):
        request_data = json.loads(self.request.body)
        keyword = request_data['keyword']
        platform = request_data['platform']
        start_date = request_data['start_date']
        end_date = request_data['end_date']
        token = request_data['token']
        re_token = param_md5(keyword + platform + start_date + end_date + 'mo')
        if re_token == token:
            return keyword, platform, start_date, end_date
        else:
            raise ValueError(u'不正常访问token')

    @run_on_executor
    def spider_hotsearch_weibo(self, start_date, end_date):
        start_ts = start_date + ' ' + '00:00:00.000'
        end_ts = end_date + ' ' + '23:59:59.999'
        hotsearch_list = []
        url = 'http://127.0.0.1:6020/rest/sql'
        headers = {
            'content-type': "text/plain"
        }
        try:
            data = "select date,keyword,searchcount from hotsearch.weibo where ts>'%s' and ts<'%s'" % (start_ts, end_ts)
            req = requests.post(url, data, headers=headers, auth=('xiaomo', '19940809')).json()
            for i in req['data']:
                hotsearch_detail = {}
                hotsearch_detail['date'] = i[0]
                hotsearch_detail['name'] = i[1]
                hotsearch_detail['value'] = int(i[2])
                hotsearch_list.append(hotsearch_detail)
        except:
            pass
        list_all_hotsearch_info = {
            'columns': ['date', 'name', 'value'],
            'hotsearch_info': hotsearch_list
        }
        return list_all_hotsearch_info


    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        try:
            keyword, platform, start_date, end_date = self.handle_args()
        except ValueError as e:
            logger.exception(e)
            self.set_status(RESPONSE_CODE.BAD_REQUEST)
            response = e.message
            self.write(response)
            self.finish()
            return

        try:
            result = yield self.spider_hotsearch_weibo(start_date, end_date)
        except ValueError as e:
            logger.exception(e)
            self.set_status(RESPONSE_CODE.INTERNAL_SERVER_ERROR)
            response = e.message
            self.write(json.dumps(response))
            self.finish()
            return

        self.set_status(RESPONSE_CODE.OK)
        response = result
        self.write(json.dumps(response))
        self.finish()