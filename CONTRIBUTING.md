# 项目贡献指南

## 说明

本文档的目的在于使有Python爬虫经验的读者在30分钟内熟悉为本项目做出贡献的方法，当原作者不再维护的时候，可以为后续维护者减轻维护门槛与负担。

### 1. 本文包含的内容

1. 添加新爬虫的方法
2. 主要接口与配置文件规范
3. 本项目中设计的常用函数工具及简要文档说明
4. 为本项目贡献的规范与建议

# 添加新ss(r)源的方法

爬虫代码在[ssshare/ss/crawler.py](https://github.com/the0demiurge/ShadowSocksShare/blob/master/ssshare/ss/crawler.py)中，配置文件在[ssshare/config.py](https://github.com/the0demiurge/ShadowSocksShare/blob/master/ssshare/config.py)中。想添加新的ss(r)源共有三种方法：

1. 对于订阅源，在配置文件中添加订阅源地址（见“主要接口与配置文件规范”一节）；
2. 对于简易网页，在配置文件中添加网页的 url（见“主要接口与配置文件规范”一节）；
3. 对于复杂爬虫，需要手动编写爬虫函数。

### 爬虫函数编写指南

本项目已经为爬虫的编写制作了一些工具，只要在[ssshare/ss/crawler.py](https://github.com/the0demiurge/ShadowSocksShare/blob/master/ssshare/ss/crawler.py)中的`main`函数之前定义一个：

- 以`crawl_`开头
- 严格按照接口规范返回值
- 不显式指定函数的输入也能正确输出结果

的函数，运行网站后就可以自动爬取帐号，并将帐号于网站上显示。

### 临时运行与测试指南

简易运行：在项目根目录中运行 ipython 或 python 终端，可以使用 `from ssshare.ss.crawler import *`引入依赖项，然后使用 ipython 或 python 终端测试运行刚写好的程序

自动测试：

- 注释掉[ssshare/config.py](https://github.com/the0demiurge/ShadowSocksShare/blob/master/ssshare/config.py)中所有其他内容
- 将[ssshare/ss/crawler.py](https://github.com/the0demiurge/ShadowSocksShare/blob/master/ssshare/ss/crawler.py)中所有其他以`crawler_`开头的函数名修改为非`crawler_`开头
- 运行`python .travis-test.py`，将运行一遍完整的爬虫和验证ss帐号的功能。由于代码运行的时候捕获并打印了所有异常，所以应当阅读终端输出的日志判断爬虫成功还是失败。
- 撤销前两步的修改

上线后的日志阅读：

heroku的dashboard中有个名为“papertrail”的app，点击这个app即可跳转到日志页。在设置中添加两个string filter，`GET`和`HEAD`，之后获取到的日志将只包含网站爬虫和错误的内容。

# 主要接口与配置文件规范

## 配置文件[ssshare/config.py](https://github.com/the0demiurge/ShadowSocksShare/blob/master/ssshare/config.py)

配置文件中有2个变量，格式均为装载着网址的list：List[Str]

- url：简易爬虫的目标网址。该爬虫只将网页源码获取到后检测 `ssr://`、`ss://`链接或图片格式的二维码，无法解析更复杂的网页。
- subscriptions：订阅源

## 爬虫函数接口

### 函数位置

函数应定义或导入于[ssshare/ss/crawler.py](https://github.com/the0demiurge/ShadowSocksShare/blob/master/ssshare/ss/crawler.py)中的`main`函数之前

### 函数命名规范

应当以`crawl_`开头，主函数将检提取所有符合此规范的函数作为爬虫函数。

### 输入参数

函数不应当设定任何必填输入参数。

### 返回值

返回2个参数，按先后顺序分别为：

- servers
- info

其中，**servers ->** List[Dict[Str:Str]]

servers是一个列表，列表的每个成员为包含ss(r)帐号关键信息的字典。字典所有的key和value都应当为字符串。

关于ss(r)关键信息的字典说明：

| key          | 是否必填 | 说明       |
| ------------ | -------- | ---------- |
| server       | 是       | 服务器地址 |
| server_port  | 是       | 服务器端口 |
| password     | 是       | 密码       |
| method       | 是       | 加密方式   |
| ssr_protocol | 否       | 协议       |
| protoparam   | 否       | 协议参数   |
| obfs         | 否       | 混淆       |
| obfsparam    | 否       | 混淆参数   |
| remarks      | 否       | 备注       |

来源网站信息**info ->** Dict[Str:Str]

来源网站信息是为了使用户能够支持提供免费ss(r)帐号而提供的信息。其中包括三个key，均为必填：

- message：来源网站提供的少量信息，比如什么时候更新的帐号，法律或免责信息等
- name：来源网站名称
- url：来源网站网址

# 本项目中设计的常用函数工具及简要文档说明

工具函数都在[ssshare/ss/parse](https://github.com/the0demiurge/ShadowSocksShare/blob/master/ssshare/ss/parse.py)中，使用的时候只需要`from ssshare.ss.parse import 函数名称`即可。

## encode， decode

输出输入都是str格式，进行urlsafe_base64编码/解码。会自动处理尾部等号。

## parse

输入 `ssr://`、`ss://`链接，输出储存本条ss帐号关键信息的字典。

## scanNetQR

输入图片地址或base64格式的二维码链接，返回解析结果（字符串）

# 为本项目贡献的建议

1. 尽可能不使用 [requirements.txt](https://github.com/the0demiurge/ShadowSocksShare/blob/master/requirements.txt) 之外安装不够方便的依赖库；
2. 尽可能不使用需要特别安装的数据库；
3. 除了对代码行长度80字符的限制可以不遵守外，代码严格按照 Google Python 编程规范执行。