#!/usr/bin/env python3
import requests


proxies = {'http': 'socks5://localhost:1080', 'https': 'socks5://localhost:1080'}


def test_socks(url='https://google.com', headers=None, proxies=proxies):
    ok = False
    try:
        ok = requests.get(url, headers=headers, proxies=proxies).ok
    except Exception as e:
        print(e)
    return ok


if __name__ == '__main__':
    print(test_socks())
