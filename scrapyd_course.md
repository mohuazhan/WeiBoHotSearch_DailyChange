## 创建项目

微博热搜爬取：
'''
root@ubuntu:~# cd /spiders
root@ubuntu:/spiders# source env_py2.7/bin/activate
(env_py2.7) root@ubuntu:/spiders# pip install --upgrade pip
(env_py2.7) root@ubuntu:/spiders# pip install Scrapy
'''
创建项目：
'''
(env_py2.7) root@ubuntu:/spiders# scrapy startproject weibohotsearch_crawler
(env_py2.7) root@ubuntu:/spiders# cd weibohotsearch_crawler
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# scrapy genspider weibohotsearch enlightent.cn
'''
启动爬虫：
'''
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# scrapy crawl weibohotsearch
'''

## Scrapyd爬虫服务器部署：

安装scrapyd:
'''
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# pip install scrapyd
'''
运行scrapyd服务：
'''
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# scrapyd
'''
在虚拟机的浏览器上访问127.0.0.1:6800即可查看当前运行项目
检查scrapyd运行状态：
'''
root@ubuntu:~# curl http://127.0.0.1:6800/daemonstatus.json
{"status": "ok", "running": 0, "finished": 0, "pending": 0, "node_name": "ubuntu"}
'''
默认配置文件位置：/spiders/env_py2.7/lib/python2.7/site-packages/scrapyd/default_scrapyd.conf
scrapyd开启远程访问：将第11行改为：bind_address = 0.0.0.0
即在其他主机上访问192.168.1.89:6800查看当前运行项目

安装scrapyd-client（安装master banch上的版本）：
'''
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# pip install --upgrade git+ssh://git@github.com/scrapy/scrapyd-client.git
'''
scrapy.cfg文件第9到14行改写如下：
# 下面的weibohotsearch为爬虫发布的名称
'''
[deploy:weibohotsearch]
# scrapyd服务器地址
url = http://192.168.1.89:6800/
project = weibohotsearch_crawler
'''
查询当前项目中全部部署目标：
'''
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# scrapyd-deploy -l
weibohotsearch       http://192.168.1.89:6800/
'''
开始打包前，执行一个命令：scrapy list ，这个命令执行成功说明可以打包了，如果没执行成功说明还有工作没完成：
'''
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# scrapy list
weibohotsearch
'''
执行打包命令：scrapyd-deploy 部署名称 -p 项目名称 -v 版本名 --build-egg=egg包名.egg：
'''
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# scrapyd-deploy weibohotsearch -p weibohotsearch_crawler -v v1.1 --build-egg=weibohotsearch.egg
'''
调用addversion.json API 将egg上传到scrapyd服务器：
'''
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# curl http://192.168.1.89:6800/addversion.json -F project=weibohotsearch -F version=v1.1 -F egg=@weibohotsearch.egg
'''

获取当前scrapyd服务器中所有已上传项目列表：
'''
root@ubuntu:~# curl 192.168.1.89:6800/listprojects.json
{"status": "ok", "projects": ["default", "weibohotsearch", "weibohotsearch_crawler"], "node_name": "ubuntu"}
'''
获取项目中可用的版本列表：
'''
root@ubuntu:~# curl 192.168.8.89:6800/listversions.json?project=weibohotsearch
{"status": "ok", "versions": ["v1_1"], "node_name": "ubuntu"}
'''
删除指定项目：
'''
root@ubuntu:~# curl 192.168.8.89:6800/delproject.json -d project=weibohotsearch_crawler
'''
加载运行指定的蜘蛛：
'''
root@ubuntu:~# curl 192.168.8.89:6800/schedule.json -d project=weibohotsearch -d spider=weibohotsearch
'''