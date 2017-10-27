#!/usr/bin/env python3
from app import *
import threading
from app.ss import ss_free, ssr_check
import requests


def test2():
    for i in range(30):
        data = requests.get('http://laptop.pythonic.life:8080/json').text
        print('data', i)
        data = data.replace('"obfs": "",', '').replace('"protocol_param": "",', '').replace('"obfs_param": "",', '').replace('"protocol": "",', '')
        w = ssr_check.test_socks_server(str_json=data)
        print('>>>>>>>结果:', w)
        if w is True:
            print(data)
        elif w == -1:
            print(data)


def test3():
    data = ss_free.main()
    for i in data:
        print(i['info'])
        for j in i['data']:
            w = ssr_check.test_socks_server(str_json=j['json'])
            print('>>>>>>>结果:', w)
            if w is True:
                print(j['json'])
            elif w == -1:
                print(j['json'])


def test4():
    data = ss_free.main(debug=['no_validate'])
    data = ssr_check.validate(data)

    for i in data:
        print(i['info'])
        for j in i['data']:
            print(j['status'])


print('-----------测试：子线程----------')
t = threading.Thread(target=test4)
t.start()
t.join()
