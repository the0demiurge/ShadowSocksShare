# ShadowSocks免费帐号共享

| **master** | **dev** |
|--------|--------|
| [![Build Status](https://travis-ci.org/the0demiurge/ShadowSocksShare-OpenShift.svg?branch=master)](https://travis-ci.org/the0demiurge/ShadowSocksShare-OpenShift) | [![Build Status](https://travis-ci.org/the0demiurge/ShadowSocksShare-OpenShift.svg?branch=dev)](https://travis-ci.org/the0demiurge/ShadowSocksShare-OpenShift) |

## 免责声明

本项目仅进行技术展示，对所爬到的帐号不负任何责任。

本项目仅面向海外华人用户，中华人民共和国境内居民禁止使用，并请立即关闭本网站！

本项目所提供的帐号均来自网络，仅供科研、学习之用。

请用本项目分享的帐号进行学习、科研，切勿用于其他用途。

请于24小时之内删掉与本项目相关的一切内容，否则出现一切问题本站作者概不负责。

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
6. 自动检测 ssr 帐号可用性


示例网站：[ss.pythonic.life](http://ss.pythonic.life)
备用地址：[ssr.pythonic.life](http://ssr.pythonic.life)

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

## Heroku 部署方法：
1. 注册 [Heroku](https://heroku.com) 
2. Fork 本项目
3. 创建一个应用：在[创建应用页面](https://dashboard.heroku.com/new-app)创建一个应用
4. 在部署 (Deploy) 页面选择 GitHub，在Connect to GitHub 这一栏连接上你的 GitHub 帐号，搜索并连接本项目
6. 环境变量添加 `PERIOD` 字段，以控制网站内容更新周期（每访问 `PERIOD` 次重新爬取信息），`PERIOD` 建议设置为`用户数量 × 5`。
7. 选择一个分支并点击 `Deploy Branch`
8. 部署完毕后，将网页拉到最上面，并点击`Open app`打开你的网站。注意：网站访问第二次之后会进行爬取并检测帐号可用性，大概花费20分钟的时间。

## OpenShift v3 部署方法：

**不再维护OpenShift版本，如果出现任何问题或有解决方案，请提交PR**

注册 OpenShift v3 之后，在创建项目中选择 Python，Python 版本选择 3.5, 之后部署的时候链接输入本项目的 https 类型的 git 链接即可。

### 编写的软件版本：

* Python 3.5
* Flask 0.12.2
* 其他，反正都安装最新版就行了

### TO DO

1. - [ ] 使用MySQL存储数据
2. - [ ] 添加留言版功能
3. - [ ] 搞定ssl证书，弄https加密
