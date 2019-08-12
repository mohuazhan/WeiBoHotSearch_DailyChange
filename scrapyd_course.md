## 创建项目

微博热搜爬取：
```
root@ubuntu:~# cd /spiders
root@ubuntu:/spiders# source env_py2.7/bin/activate
(env_py2.7) root@ubuntu:/spiders# pip install --upgrade pip
(env_py2.7) root@ubuntu:/spiders# pip install Scrapy
```
创建项目：
```
(env_py2.7) root@ubuntu:/spiders# scrapy startproject weibohotsearch_crawler
(env_py2.7) root@ubuntu:/spiders# cd weibohotsearch_crawler
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# scrapy genspider weibohotsearch enlightent.cn
```
启动爬虫：
```
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# scrapy crawl weibohotsearch
```

## Scrapyd部署爬虫：

安装scrapyd:
```
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# pip install scrapyd
```
运行scrapyd服务：
```
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# scrapyd
```
在虚拟机的浏览器上访问127.0.0.1:6800即可查看当前运行项目
检查scrapyd运行状态：
```
root@ubuntu:~# curl http://127.0.0.1:6800/daemonstatus.json
{"status": "ok", "running": 0, "finished": 0, "pending": 0, "node_name": "ubuntu"}
```
默认配置文件位置：/spiders/env_py2.7/lib/python2.7/site-packages/scrapyd/default_scrapyd.conf
scrapyd开启远程访问：将第11行改为：bind_address = 0.0.0.0
即在其他主机上访问192.168.1.89:6800查看当前运行项目

安装scrapyd-client（安装master banch上的版本）：
```
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# pip install --upgrade git+ssh://git@github.com/scrapy/scrapyd-client.git
```
scrapy.cfg文件第9到14行改写如下：
```
# 下面的weibohotsearch为爬虫发布的名称
[deploy:weibohotsearch]
# scrapyd服务器地址
url = http://192.168.1.89:6800/
project = weibohotsearch_crawler
```
查询当前项目中全部部署目标：
```
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# scrapyd-deploy -l
weibohotsearch       http://192.168.1.89:6800/
```
开始打包前，执行一个命令：scrapy list ，这个命令执行成功说明可以打包了，如果没执行成功说明还有工作没完成：
```
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# scrapy list
weibohotsearch
```
执行打包命令：scrapyd-deploy 部署名称 -p 项目名称 -v 版本名 --build-egg=egg包名.egg：
```
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# scrapyd-deploy weibohotsearch -p weibohotsearch_crawler -v v1.1 --build-egg=weibohotsearch.egg
```
调用addversion.json API 将egg上传到scrapyd服务器：
```
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# curl http://192.168.1.89:6800/addversion.json -F project=weibohotsearch -F version=v1.1 -F egg=@weibohotsearch.egg
```

获取当前scrapyd服务器中所有已上传项目列表：
```
root@ubuntu:~# curl 192.168.1.89:6800/listprojects.json
{"status": "ok", "projects": ["default", "weibohotsearch", "weibohotsearch_crawler"], "node_name": "ubuntu"}
```
获取项目中可用的版本列表：
```
root@ubuntu:~# curl 192.168.1.89:6800/listversions.json?project=weibohotsearch
{"status": "ok", "versions": ["v1_1"], "node_name": "ubuntu"}
```
删除指定项目：
```
root@ubuntu:~# curl 192.168.1.89:6800/delproject.json -d project=weibohotsearch_crawler
```
加载运行指定的蜘蛛：
```
root@ubuntu:~# curl 192.168.1.89:6800/schedule.json -d project=weibohotsearch -d spider=weibohotsearch
```

## ubuntu搭建scrapyd爬虫服务器

创建scrapyd.service文件，内容如下：
```
[Unit]
Description=scrapyd
After=network.target
Documentation=http://scrapyd.readthedocs.org/en/latest/api.html

[Service]
User=root
# /spiders/env_py2.7/bin/scrapyd是scrapyd启动项所在路径，/spiders/weibohotsearch_crawler/scrapyd.log作为日志
ExecStart=/spiders/env_py2.7/bin/scrapyd --logfile /spiders/weibohotsearch_crawler/scrapyd.log

[Install]
WantedBy=multi-user.target
```
检查系统是否安装systemd：
```
root@ubuntu:~# systemd --version
```
将scrapyd.service文件放到/lib/systemd/system下，同时也备份一份在/spiders/weibohotsearch_crawler/other_profile下
在ubuntu中启动scrapyd：
```
root@ubuntu:~# sudo systemctl start scrapyd
```
或者：
```
root@ubuntu:~# sudo service scrapyd start
```
这时修改了一下scrapyd.service文件，重新载入systemd，扫描新的或有变动的单元：
```
root@ubuntu:~# systemctl daemon-reload
```
重新启动：
```
root@ubuntu:~# sudo systemctl restart scrapyd
```
检查服务状态：
```
root@ubuntu:~# sudo systemctl status scrapyd
```
让scrapyd随同开机启动：
```
root@ubuntu:~# sudo systemctl enable scrapyd
Created symlink from /etc/systemd/system/multi-user.target.wants/scrapyd.service to /lib/systemd/system/scrapyd.service.
```
取消开机启动：
```
root@ubuntu:~# sudo systemctl disable scrapyd
```

## scrapyd服务器添加认证信息

安装Nginx：
```
root@ubuntu:~# sudo apt-get install nginx
```
启动Nginx：
```
root@ubuntu:~# /etc/init.d/nginx start
```
现在在浏览器访问192.168.1.89或192.168.1.89:80都可以看到Welcome to nginx!的页面
关闭Nginx：
```
root@ubuntu:~# /etc/init.d/nginx stop
```
在/etc/nginx/sites-enabled/下创建scrapyd的nginx配置文件，命名为：scrapyd_nginx.conf，配置内容如下（同时也备份一份在/spiders/weibohotsearch_crawler/other_profile下）：
```
# Scrapyd local proxy for basic authentication.
# Don't forget iptables rule.
# iptables -A INPUT -p tcp --destination-port 6800 -s ! 127.0.0.1 -j DROP

server {
	listen 6801;
	location / {
		proxy_pass            http://127.0.0.1:6800/;
		auth_basic            "Restricted";
		auth_basic_user_file  /etc/nginx/conf.d/.htpasswd;
	}
}
```

安装htpasswd（htpasswd是开源http服务器apache httpd的一个命令工具，用于生成http基本认证的密码文件）：
```
root@ubuntu:~# sudo apt-get install apache2-utils
nginx使用htpasswd创建用户认证：
root@ubuntu:~# cd /etc/nginx/conf.d
root@ubuntu:/etc/nginx/conf.d# sudo htpasswd -c .htpasswd xiaomo
New password: 19940809	（密码输入时隐藏）
Re-type new password: 19940809	（密码输入时隐藏）
Adding password for user xiaomo
```
查看认证：
```
root@ubuntu:/etc/nginx/conf.d# cat .htpasswd
xiaomo:$apr1$OQfgR7QI$NhEPPVecFDricSDPLihSH/
```
重启nginx：
```
root@ubuntu:~# /etc/init.d/nginx restart
```
访问192.168.1.89:6801，输入账号：xiaomo	密码：19940809，即可进入scrapyd控制台

修改scrapy.cfg文件部分代码：
```
# 下面的weibohotsearch为爬虫发布的名称
[deploy:weibohotsearch]
# scrapyd服务器地址
url = http://192.168.1.89:6801/
project = weibohotsearch_crawler
username = xiaomo
password = 19940809
```
最后修改scrapyd的配置bind_address字段为127.0.0.1，以免可以从外面绕过nginx，直接访问6800端口：
打开/spiders/env_py2.7/lib/python2.7/site-packages/scrapyd/default_scrapyd.conf：
将第11行改为：bind_address = 127.0.0.1

重启scrapyd：
```
root@ubuntu:~# sudo systemctl restart scrapyd
```
这时打开浏览器可成功访问192.168.1.89:6801，但已无法访问192.168.1.89:6800

这时把之前打包的爬虫文件删除，重新执行打包命令：
```
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# scrapyd-deploy weibohotsearch -p weibohotsearch_crawler -v v1.1 --build-egg=weibohotsearch.egg
```
此时调用addversion.json API 将egg上传到scrapyd服务器时，需要带上身份认证：
```
(env_py2.7) root@ubuntu:/spiders/weibohotsearch_crawler# curl -u xiaomo:19940809 http://192.168.1.89:6801/addversion.json -F project=weibohotsearch -F version=v1.1 -F egg=@weibohotsearch.egg
```
