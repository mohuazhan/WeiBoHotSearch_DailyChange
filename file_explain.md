# 文件说明

- /：项目根目录
	- scrapy.cfg：scrapy运行配置
	- file_explain.md：文件说明
	- scrapyd_course.md：scrapyd相关配置教程
- /weibohotsearch_crawler：爬虫项目
	- /spiders：爬取主代码
- /crawl_common：爬虫加载项
	- manual_getdate.py：手动获得日期
	- user_agents.py：存放user_agent列表
- /other_profile：其他配置文件
	- scrapyd.service：systemd启动scrapyd配置
	- scrapyd_nginx.conf：scrapyd的nginx配置
- scrapyd生成项目文件：
	- /build
	- /project.egg-info
	- setup.py
	- weibohotsearch.egg