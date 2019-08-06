# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.http import Request
from ..items import WeibohotsearchCrawlerItem
from user_agents import get_agent
import json
from scrapy.shell import inspect_response


class WeibohotsearchSpider(Spider):
    name = 'weibohotsearch'
    base_url = "https://www.enlightent.cn/research/top/getWeiboHotSearchDayAggs.do?date=%s"
    date_list = ['2019/8/2','2019/8/3']
    start_urls = [base_url % date for date in date_list]

    def parse(self, response):
        hotsearch = json.loads(response.body)
        for item in hotsearch:
            hotsearch_item = WeibohotsearchCrawlerItem()
            date = response.url.replace('https://www.enlightent.cn/research/top/getWeiboHotSearchDayAggs.do?date=', '')
            hotsearch_item['date'] = date
            hotsearch_item['keyword'] = item['keyword']
            hotsearch_item['url'] = item['url']
            hotsearch_item['count'] = item['count']
            hotsearch_item['searchCount'] = item['searchCount']
            hotsearch_item['rank'] = item['rank']

            yield hotsearch_item
