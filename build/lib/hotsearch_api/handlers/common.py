# -*- coding: utf-8 -*-

import logging
from tornado.web import RequestHandler
from concurrent.futures import ThreadPoolExecutor

from consts import RESPONSE_CODE, RESPONSE_MSG

logger = logging.getLogger(__name__)


class CommonHandler(RequestHandler):

    executor = ThreadPoolExecutor(8)


    def set_default_headers(self):
        # 解决服务端跨域的问题
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        # 前后端分离，前端使用vue，会发一个options请求，后台就需要实现这个options方法
        self.set_status(204)
        self.finish()


    def __init__(self, *args, **kwargs):
        super(CommonHandler, self).__init__(*args, **kwargs)
        self.response_body = dict()

    def initialize(self, *args, **kwargs):
        self.response_body = {
            'msg': RESPONSE_MSG.OK
        }
        logger.info('Handling uri: %s', self.request.uri)

    def verify_headers_accept(self):
        try:
            accept = self.request.headers['Accept']
        except KeyError as e:
            logger.exception(e)
            self.response_body['msg'] = RESPONSE_MSG.BAD_REQUEST
            return False

        if accept is None or '*/*' in accept:
            self.set_header('Content-Type',
                            'application/json; charset="utf-8"')
        elif 'application/json' in accept:
            self.set_header('Content-Type',
                            'application/json; charset="utf-8"')
        else:
            self.response_body['msg'] = RESPONSE_MSG.BAD_REQUEST
            logger.warning(self.response_body['msg'])
            return False
        return True

    def verify_headers(self):
        if not self.verify_headers_accept():
            self.set_status(RESPONSE_CODE.BAD_REQUEST)
            return False
        return True

    def verify_body(self):
        return True

    def verify(self):
        if not (self.verify_headers() and self.verify_body()):
            return False
        return True
