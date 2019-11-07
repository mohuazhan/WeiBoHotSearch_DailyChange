# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import taos
import pymongo
import MySQLdb
import treq  # 相当于基于Twisted应用编写的Python requests包，用于执行HTTP请求
from twisted.internet import defer

class WeibohotsearchCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonFeedPipeline(object):  # 数据导出为json文件
    def __init__(self):
        self.json_file = open('feed.json', 'wt')
        self.json_file.write("[\n")
    
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.json_file.write(line)
        return item
    
    def close_spider(self, spider):
        self.json_file.write("\n]")
        self.json_file.close()


class TDenginePipeline(object):  # 数据导出到TDengine
    def __init__(self, TDengine_host, TDengine_user, TDengine_password, TDengine_database):
        self.TDengine_host = TDengine_host
        self.TDengine_user = TDengine_user
        self.TDengine_password = TDengine_password
        self.TDengine_database = TDengine_database

    @classmethod
    def from_settings(cls, settings):
        return cls(
            TDengine_host = settings['TDENGINE_HOST'],
            TDengine_user = settings['TDENGINE_USER'],
            TDengine_password = settings['TDENGINE_PASSWORD'],
            TDengine_database = settings['TDENGINE_DATABASE']
        )

    def open_spider(self, spider):
        # 连接TDengine
        self.TDengine_conn = taos.connect(
            host = self.TDengine_host,
            user = "%s" % self.TDengine_user,
            password = "%s" % self.TDengine_password,
            database = self.TDengine_database
        )
        # 获取操作游标
        self.TDengine_cursor = self.TDengine_conn.cursor()

    def close_spider(self, spider):
        self.TDengine_conn.close()

    def process_item(self, item, spider):
        # 批量写入
        try:
            self.TDengine_cursor.execute("insert into weibo values ('%s', '%s', '%s', '%s', %d, %d, %d)" % (item['ts'], item['date'], item['keyword'], item['url'], item['wbcount'], item['searchcount'], item['rank']))
        except Exception as err:
            raise(err)
        return item


class MongoDBPipeline(object):  # 数据导出到MongoDB
    def __init__(self, MongoDB_server, MongoDB_port, MongoDB_user, MongoDB_password, MongoDB_db, MongoDB_collection):
        # 连接MongoDB
        client = pymongo.MongoClient(MongoDB_server, MongoDB_port)
        database = client.admin  # 连接用户库
        database.authenticate(MongoDB_user, MongoDB_password)  # 用户认证
        database = client[MongoDB_db]  # 连接数据库
        self.collection = database[MongoDB_collection]  # 连接数据表

    @classmethod
    def from_settings(cls, settings):
        return cls(
            MongoDB_server = settings['MONGODB_SERVER'],
            MongoDB_port = settings['MONGODB_PORT'],
            MongoDB_user = settings['MONGODB_USER'],
            MongoDB_password = settings['MONGODB_PASSWORD'],
            MongoDB_db = settings['MONGODB_DB'],
            MongoDB_collection = settings['MONGODB_COLLECTION']
        )

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class MySQLPipeline(object):  # 数据导出到MySQL
    def __init__(self, MySQL_host, MySQL_port, MySQL_user, MySQL_password, MySQL_db, MySQL_table):
        self.MySQL_host = MySQL_host
        self.MySQL_port = MySQL_port
        self.MySQL_user = MySQL_user
        self.MySQL_password = MySQL_password
        self.MySQL_db = MySQL_db
        self.MySQL_table = MySQL_table

    @classmethod
    def from_settings(cls, settings):
        return cls(
            MySQL_host = settings['MYSQL_HOST'],
            MySQL_port = settings['MYSQL_PORT'],
            MySQL_user = settings['MYSQL_USER'],
            MySQL_password = settings['MYSQL_PASSWORD'],
            MySQL_db = settings['MYSQL_DB'],
            MySQL_table = settings['MYSQL_TABLE']
        )

    def open_spider(self, spider):
        # 连接MySQL
        self.MySQL_conn = MySQLdb.connect(
            host = self.MySQL_host, 
            port = self.MySQL_port, 
            user = self.MySQL_user, 
            passwd = self.MySQL_password, 
            db = self.MySQL_db,
            charset='utf8' 
        )
        # 获取操作游标
        self.MySQL_cursor = self.MySQL_conn.cursor()

    def close_spider(self, spider):
        self.MySQL_conn.close()

    def process_item(self, item, spider):
        self.MySQL_cursor.execute("insert into %s (date, keyword, url, wbcount, searchcount, rank) values ('%s', '%s', '%s', %d, %d, %d)" % (self.MySQL_table, item['date'], item['keyword'], item['url'], item['wbcount'], item['searchcount'], item['rank']))
        self.MySQL_conn.commit()
        return item


class EsPipeline(object): # 数据导出到Elasticsearch
    def __init__(self, es_url):
        self.es_url = es_url

    @classmethod
    def from_settings(cls, settings):
        return cls(
            es_url = settings['ES_URL']
        )

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        try:
            data = json.dumps(dict(item), ensure_ascii=False).encode("utf-8")
            yield treq.post(self.es_url, data, headers={b'Content-Type': [b'application/json']})
        finally:
            defer.returnValue(item)