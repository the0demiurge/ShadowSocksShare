#!/usr/bin/env python3
import requests
import time
import threading
from ssshare.ss import ss_local
import random


def test_connection(
        url='http://ip.cn',
        headers={'User-Agent': 'curl/7.21.3 (i686-pc-linux-gnu) '
                 'libcurl/7.21.3 OpenSSL/0.9.8o zlib/1.2.3.4 libidn/1.18'},
        proxies=None, port=1080, timeout=10):
    if not proxies:
        proxies = {'http': 'socks5://localhost:{}'.format(port),
                   'https': 'socks5://localhost:{}'.format(port)}
    ok = False
    content = ''
    try:
        respond = requests.get(url, headers=headers,
                               proxies=proxies, timeout=timeout)
        ok = respond.ok
        content = respond.text
    except Exception as e:
        print(e)
    return ok, content


def test_socks_server(dictionary=None, str_json=None, port=None):
    if not port:
        port = random.randint(2000, 3000)
    try:
        try:
            loop, tcps, udps = ss_local.main(
                dictionary=dictionary, str_json=str_json, port=port)
        except Exception as e:
            print(e)
            return -1, 'SSR start failed'
        try:
            t = threading.Thread(target=loop.run)
            t.start()
            time.sleep(3)
            conn, content = test_connection(port=port)
            loop.stop()
            t.join()
            tcps.close(next_tick=True)
            udps.close(next_tick=True)
            time.sleep(1)
            return conn, content
        except Exception as e:
            print(e)
            return -2, 'Thread or Connection to website failed'
    except SystemExit as e:
        return e.code - 10, 'Unknown failure'


def validate(websites):
    for servers in websites:
        print(servers['info'])
        for server in servers['data']:
            result, info = test_socks_server(str_json=server['json'])
            print('>' * 10, '结果:', result)
            if result is True:
                print('>' * 10, '测试通过！')
            elif result == -1:
                print(server['json'])
            server['status'] = result
            server['content'] = info
    return websites


if __name__ == '__main__':
    print(test_connection())
