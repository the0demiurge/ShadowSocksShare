# ShadowSocks免费帐号共享

| **master** | **dev** |
|--------|--------|
| [![Build Status](https://travis-ci.org/the0demiurge/ShadowSocksShare-OpenShift.svg?branch=master)](https://travis-ci.org/the0demiurge/ShadowSocksShare-OpenShift) | [![Build Status](https://travis-ci.org/the0demiurge/ShadowSocksShare-OpenShift.svg?branch=dev)](https://travis-ci.org/the0demiurge/ShadowSocksShare-OpenShift) |

## 简介：

本项目是我的 [Python 实验室](https://github.com/the0demiurge/Python-Scripts)子模块，欢迎大家 STAR/FORK/ISSUE/提交 PR ～

本网站的功能是从网上爬下来各种免费 ss(r) 帐号，重新解析和分发，可以在 ssr 客户端。这个网站是我已知**唯一一个提供 ssr 订阅服务**的了。

*我不生产 ss(r) 帐号，我只是帐号的搬运工。不保证可用，不保证速度，不保证安全，不保证隐私。*


### 功能：

1. 二维码
2. ss(r) 分享URL
3. json 配置
4. **ssr 订阅和 json 配置订阅**
5. **自动更新爬虫数据**


示例网站：[ss.pythonic.life](http://ss.pythonic.life)

博客连接：[the0demiurge.blogspot.jp](https://the0demiurge.blogspot.jp/2017/07/shadowsocks.html)

### 为该项目贡献力量：
本项目的作者和用户们为您的所有贡献表示由衷的感谢！

为本项目添砖加瓦，您可以：

以非技术方式：

1. 反馈建议：到[这个页面](https://github.com/the0demiurge/ShadowSocksShare-OpenShift/issues)提交Issue
2. 提供比较好的 ss(r) 分享链接
3. 捐助我：如果你已经可以上 Google，打开[示例网站](http://ss.pythonic.life)并拖到最后，就能看到微信打赏二维码：）

以技术类方式：

1. Fork 本项目并优化本项目
2. 提交 Pull Requests

## 用法：
本地运行：

`python manage.py runserver`

## OpenShift v3 部署方法：

**不再维护OpenShift版本，如果出现任何问题或有解决方案，请提交PR**

注册 OpenShift v3 之后，在创建项目中选择 Python，Python 版本选择 3.5, 之后部署的时候链接输入本项目的 https 类型的 git 链接即可。

## Heroku 部署方法：
1. 注册 Heroku 并安装 heroku 的命令行工具，登陆上，不用多说了吧，免费。具体操作请阅读[Heroku 指南（官方英文版）](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)
2. 下载本项目：`git clone https://github.com/the0demiurge/ShadowSocksShare-OpenShift.git`
3. 进入项目目录：`cd ShadowSocksShare-OpenShift`
4. 创建一个 heroku 应用：`heroku create`
5. 部署到云端：`git push heroku master`
6. 打开部署好的网站：`heroku open`

### 编写的软件版本：

* Python 3.5
* Flask 0.12.2
* 其他，反正都安装最新版就行了

### TO DO
当前已知问题：
1. - [ ]  没有做ss账号失效检测
2. - [ ] 非ssr的账号也可以放到订阅里面，只不过需要转变格式
3. - [ ] 输出的JSON格式的文件有问题，如果是非ssr账号，Python客户端会不认
4. - [ ] 性能不太强
5. - [ ] 最近为了弄ssl证书把DNS弄得很乱，所以另起炉灶换了域名，新域名为SSR.pythonic.life，现在原域名会重定向到新域名。

如果域名都不好使，请使用备用网址：
http://ssshare-ssshare.7e14.starter-us-west-2.openshiftapps.com/

除了修复问题，下一步准备做：
1. - [ ] 使用MySQL存储数据
2. - [ ] 添加留言版功能
3. - [ ] 搞定ssl证书，弄https加密
