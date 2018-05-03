#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 页面中含有ss://连接的url
url = [
    'https://plus.google.com/communities/104092405342699579599/stream/8a593591-2091-4096-bb00-7d9c5659db93',
    'https://plus.google.com/communities/109204483693184691558',
    'https://plus.google.com/communities/117702818760720009772/stream/47c69db4-9362-4d91-a017-97f3be948437',
    'https://plus.google.com/communities/107859708371989171939',
    'http://www.ssr.blue/',
]


# 日志文件路径
LOG_FILENAME = './logging.out'

# 请求头
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

REDIS_KEY = 'proxies'

# SS代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

VALID_STATUS_CODES = [200, 302]

# SS代理池数量界限
POOL_UPPER_THRESHOLD = 50000

# 检查周期
TESTER_CYCLE = 2000

# 获取周期
GETTER_CYCLE = 3000

# 测试API
TEST_URL = 'http://www.baidu.com'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 8080

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 10