#!/usr/bin/env python3
import socks
import socket
import requests


s = socket.socket

def test_socks(url='https://google.com', headers=None):
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
    socket.socket = socks.socksocket
    ok = False
    try:
        ok = requests.get(url, headers=headers).ok
    except Exception as e:
        print(e)
    socket.socket = s
    return ok

