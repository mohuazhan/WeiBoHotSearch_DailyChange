# -*- coding: utf-8 -*-

from handlers.spider_hotsearch import WeiboHotsearchHandler


# 访问地址
ROUTE_HOTSEARCH_WEIBO = r'/v1/spider/hotsearch/weibo'


# 映射列表
routes = [
    (ROUTE_HOTSEARCH_WEIBO, WeiboHotsearchHandler),
]
