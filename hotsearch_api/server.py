# -*- coding: utf-8 -*-

import logging
import os
from tornado import web, ioloop, autoreload
from tornado.options import options, define

from routes import routes


define('host', default='127.0.0.1', help='the ip listening on', type=str)
define('port', default=8888, help='run on the given port', type=int)
define('log_path', default='./tmp_logs', help='log path ', type=str)

# 在未使用Supervisor部署时，可通过以下方式设置日志路径
# logging.basicConfig(
#     filename='%s/tornado.log' % options.log_path,
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     )


def make_app():
    return web.Application(
        routes,
        debug=False,
        # static_path=os.path.join(os.path.dirname(__file__), "static")  # 静态目录访问
    )


def start_server():
    options.parse_command_line()
    app = make_app()
    try:
        app.listen(options.port, address=options.host)
        loop = ioloop.IOLoop.instance()
        # autoreload.start(loop)
        loop.start()
    except KeyboardInterrupt:
        print 'Server terminated by User.'


if __name__ == '__main__':
    start_server()
