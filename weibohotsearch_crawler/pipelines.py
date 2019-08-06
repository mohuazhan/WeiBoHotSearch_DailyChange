# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json


class WeibohotsearchCrawlerPipeline:
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
