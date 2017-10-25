#!/usr/bin/env python3
import requests
import time
import threading
from app.ss import ss_local


def test_connection(url='https://google.com', headers=None, proxies=None, port=1080):
    if not proxies:
        proxies = {'http': 'socks5://localhost:{}'.format(port),
                   'https': 'socks5://localhost:{}'.format(port)}
    ok = False
    try:
        ok = requests.get(url, headers=headers, proxies=proxies).ok
    except Exception as e:
        print(e)
    return ok


def test_socks_server(data):
    loop, tcps, udps = ss_local.main(data, 2001)
    t = threading.Thread(target=loop.run)
    t.start()
    time.sleep(3)
    conn = test_connection(port=2001)
    loop.stop()
    t.join()
    tcps.close(next_tick=True)
    udps.close(next_tick=True)
    time.sleep(2)
    return conn


if __name__ == '__main__':
    print(test_connection())
