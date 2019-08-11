# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import taos
import json


class WeibohotsearchCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


# class JsonFeedPipeline(object):  # 数据导出为json文件
#     def __init__(self):
#         self.json_file = open('feed.json', 'wt')
#         self.json_file.write("[\n")
#     
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + ",\n"
#         self.json_file.write(line)
#         return item
#     
#     def close_spider(self, spider):
#         self.json_file.write("\n]")
#         self.json_file.close()


# class TDenginePipeline(object):  # 数据导出到TDengine
    # def __init__(self, TDengine_host, TDengine_user, TDengine_password, TDengine_database):
        # self.TDengine_host = TDengine_host
        # self.TDengine_user = TDengine_user
        # self.TDengine_password = TDengine_password
        # self.TDengine_database = TDengine_database

    # @classmethod
    # def from_settings(cls, settings):
        # return cls(
            # TDengine_host = settings['TDENGINE_HOST'],
            # TDengine_user = settings['TDENGINE_USER'],
            # TDengine_password = settings['TDENGINE_PASSWORD'],
            # TDengine_database = settings['TDENGINE_DATABASE']
        # )

    # def open_spider(self, spider):
        # # 连接TDengine
        # self.TDengine_conn = taos.connect(
            # host=self.TDengine_host,
            # user="%s" % self.TDengine_user,
            # password="%s" % self.TDengine_password,
            # database=self.TDengine_database
        # )
        # # 获取操作游标
        # self.TDengine_cursor = self.TDengine_conn.cursor()

    # def close_spider(self, spider):
        # self.TDengine_conn.close()

    # def process_item(self, item, spider):
        # # 批量写入
        # try:
            # self.TDengine_cursor.execute("insert into weibo values (now, '%s', '%s', '%s', %d, %d, %d)" % (item['date'], item['keyword'], item['url'], item['wbcount'], item['searchcount'], item['rank']))
        # except Exception as err:
            # self.TDengine_conn.close()
            # raise(err)
        # return item
