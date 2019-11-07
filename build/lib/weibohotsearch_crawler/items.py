# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class WeibohotsearchCrawlerItem(Item):
    ts = Field()  # 精确到毫秒的时间(导入TDengine时所需)
    date = Field()  # 日期
    keyword = Field()  # 关键词
    url = Field()  # 地址
    wbcount = Field()  # 相关微博数
    searchcount = Field()  # 搜索数
    rank = Field()  # 排名
