#!/usr/bin/env python3
import requests
import time
import threading
from app.ss import ss_local


def test_connection(url='https://google.com', headers=None, proxies=None, port=1080, timeout=10):
    if not proxies:
        proxies = {'http': 'socks5://localhost:{}'.format(port),
                   'https': 'socks5://localhost:{}'.format(port)}
    ok = False
    try:
        ok = requests.get(url, headers=headers, proxies=proxies, timeout=timeout).ok
    except Exception as e:
        print(e)
    return ok


def test_socks_server(dictionary=None, str_json=None, port=2001):
    try:
        try:
            loop, tcps, udps = ss_local.main(dictionary=dictionary, str_json=str_json, port=port)
        except Exception as e:
            return -1
        try:
            t = threading.Thread(target=loop.run)
            t.start()
            time.sleep(2)
            conn = test_connection(port=2001)
            loop.stop()
            t.join()
            tcps.close(next_tick=True)
            udps.close(next_tick=True)
            time.sleep(1)
            return conn
        except Exception as e:
            return -2
    except SystemExit as e:
        return e.code - 10


if __name__ == '__main__':
    print(test_connection())
