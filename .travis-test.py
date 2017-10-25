#!/usr/bin/env python3
from app import *
from app.ss import ss_free, test_ss
ss_free.main()

data = '''{
  "password": "f42c35a7d06f",
  "local_address": "127.0.0.1",
  "workers": 1,
  "local_port": 1080,
  "timeout": 300,
  "udp_timeout": 60,
  "server_port": 443,
  "group": "Charles Xu",
  "server_ipv6": "::",
  "method": "AES-256-CFB",
  "server": "169.46.31.82"
}
'''

assert test_ss.test_socks_server(str_json=data) is True, 'ssr test failed!'
