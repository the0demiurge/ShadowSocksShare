# ShadowSocks免费帐号共享

简介：其实没啥好介绍的，就是一个很简单的HTML解析而已。

示例网站：[ss.pythonic.life](http://ss.pythonic.life)

博客连接：[the0demiurge.blogspot.jp](https://the0demiurge.blogspot.jp/2017/07/shadowsocks.html)

### 用法：
`python manage.py runserver`

### OpenShift部署方法：

* 创建一个应用 `rhc app create ssshare python-3.3`
* 下载本代码 `git clone https://github.com/the0demiurge/Python-Scripts.git`
* 下载OpenShift项目 `git clone ssh://project-git-uri ssshare`
* 直接将源码复制到OpenShift项目中 `cp -r Python-Scripts/src/Web/Flask/ShadowSocksShare/* ssshare/`
* 提交修改 `cd ssshare;git add -A;git commit -m 'added ssshare';git push`

### 编写的软件版本：

* Python 3.5
* Flask 0.12.2
* 其他，反正都安装最新版就行了

免费帐号来源：[这个GitHub项目](https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7)
