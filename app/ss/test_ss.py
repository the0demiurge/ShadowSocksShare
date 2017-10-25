#!/usr/bin/env python3
import requests


def test_socks(url='https://google.com', headers=None, proxies=None, port=1080):
    if not proxies:
        proxies = {'http': 'socks5://localhost:{}'.format(port),
         'https': 'socks5://localhost:{}'.format(port)}
    ok = False
    try:
        ok = requests.get(url, headers=headers, proxies=proxies).ok
    except Exception as e:
        print(e)
    return ok



###################################3

from app.ss import test_ss
import time
from app.ss import ss_local
import threading

data = '''
{
  "password": "f42c35a7d06f",
  "fast_open": false,
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

def test(data):
    loop, tcps, udps = ss_local.main(data, 2000)
    t = threading.Thread(target=loop.run)

    t.start()
    time.sleep(3)
    print('测试联通状况：')
    print('连接情况', test_ss.test_socks(url='http://ip.cn',port=2000))
    loop.stop()
    tcps.close(next_tick=True)
    udps.close(next_tick=True)
    print('stopped')
    time.sleep(2)





########################################



if __name__ == '__main__':
    print(test_socks())
    test(data)
    test(data)

    for i in range(10):
        time.sleep(60)
        print('sleeped:', i)
