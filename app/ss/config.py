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



LOG_FILENAME = 'logging_example.out'

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
TIMEOUT = 5
PROXIES = {
    'http': "127.0.0.1:1085",
    'https': "127.0.0.1:1085",
}
