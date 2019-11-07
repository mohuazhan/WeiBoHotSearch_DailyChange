# -*- coding: utf-8 -*-

# Scrapy settings for weibohotsearch_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weibohotsearch_crawler'

SPIDER_MODULES = ['weibohotsearch_crawler.spiders']
NEWSPIDER_MODULE = 'weibohotsearch_crawler.spiders'

# 数据存储为json文件
# FEED_URI = 'result.json'

# 设置序列化格式为json
FEED_FORMAT = 'json'

# 配置数据导出到TDengine
TDENGINE_HOST = '127.0.0.1'
TDENGINE_USER = 'xiaomo'
TDENGINE_PASSWORD = '19940809'
TDENGINE_DATABASE = 'hotsearch'

# 配置数据导出到MongoDB
MONGODB_SERVER = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_USER = 'xiaomo'
MONGODB_PASSWORD = '19940809'
MONGODB_DB = "hotsearch"
MONGODB_COLLECTION = "weibo"

# 配置数据导出到MySQL
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'xiaomo'
MYSQL_PASSWORD = 'mhz$940809$'
MYSQL_DB = "hotsearch"
MYSQL_TABLE = "weibo"

# 配置数据导出到Elasticsearch
ES_URL = 'http://127.0.0.1:9200/hotsearch/weibo'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'weibohotsearch_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'weibohotsearch_crawler.middlewares.WeibohotsearchCrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'weibohotsearch_crawler.middlewares.WeibohotsearchCrawlerDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'weibohotsearch_crawler.pipelines.WeibohotsearchCrawlerPipeline': 300,
#     'weibohotsearch_crawler.pipelines.JsonFeedPipeline': 301,
    'weibohotsearch_crawler.pipelines.TDenginePipeline': 302,
#     'weibohotsearch_crawler.pipelines.MongoDBPipeline': 303,
#     'weibohotsearch_crawler.pipelines.MySQLPipeline': 304,
#     'weibohotsearch_crawler.pipelines.EsPipeline': 305,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
