#!/usr/bin/env python3
from ssshare import *
import threading
from ssshare.ss import crawler, ssr_check
import requests


def test2():
    data = '''
{
  "server": "203.104.205.115",
  "server_ipv6": "::",
  "server_port": 8080,
  "local_address": "127.0.0.1",
  "local_port": 1080,
  "password": "yui",
  "group": "Charles Xu",
  "obfs": "tls1.2_ticket_auth",
  "method": "chacha20",
  "ssr_protocol": "auth_sha1_v4",
  "obfsparam": "",
  "protoparam": ""
}'''
    w = ssr_check.test_socks_server(str_json=data)
    print('>>>>>>>结果:', w)
    if w is True:
        print(data)
    elif w == -1:
        print(data)
        raise Exception('sodium test failed')



print('-----------测试：子线程----------')
t = threading.Thread(target=test2)
t.start()
t.join()
