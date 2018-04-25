#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Storing sites or functions that not working anymore... maybe"""
from bs4 import BeautifulSoup
import requests
import logging
import regex as re





def request_newpac(url='https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7'):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    ss_list = list()

    for i in soup.find_all('p'):
        if re.match('\<p\>\s*服务器\d+[^:：]*[:：]', str(i)):
            ss_list.append(str(i))

    servers = list()
    for i in ss_list:
        servers.append(dict())
        servers[-1]['string'] = i
        # name
        tmp = re.findall('服务器\d+[^:：]*(?=\s*[:：])', i)
        if tmp:
            servers[-1]['remarks'] = tmp[0]

        # server
        tmp = re.findall('(?<=服务器\s*\d+[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[\w\d\.]+', i)
        if tmp:
            servers[-1]['server'] = tmp[0]

        # server_port
        tmp = re.findall('(?<=端口\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)\d+', i)
        if tmp:
            servers[-1]['server_port'] = tmp[0]

        # password
        tmp = re.findall('(?<=密码\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['password'] = tmp[0]

        # method
        tmp = re.findall('(?<=加密方[式法]\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['method'] = tmp[0]

        # SSR协议
        tmp = re.findall('(?<=SSR协议\s*[^:：]*[:：]\s*[^a-zA-Z_0-9]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['ssr_protocol'] = tmp[0]

        # 混淆
        tmp = re.findall('(?<=混淆\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['obfs'] = tmp[0]
    info = {'message': '', 'name': 'new-pac', 'url': url}
    return servers, info


def request_nobey(url='https://raw.githubusercontent.com/NoBey/Shadowsocks-free/master/README.md'):
    def strip_dot(x):
        return
    print('req nobey...')
    servers = list()
    try:
        data = re.split('##+|---+', requests.get(url).text)[2:5:2]
        info = {'message': '', 'name': 'NoBey', 'url': 'https://github.com/NoBey/Shadowsocks-free'}

        for i, server in enumerate(data):
            server = server.split('\n')

            name = server[0].strip()
            (
                ips,
                ports,
                _,
                method,
                password) = list(map(
                    lambda server: list(map(
                        lambda x: x.strip().strip('`').strip(),
                        server.strip('-').strip().split()[1:])),
                    server[1:6]))
            method = method[0]
            password = password[0]

            for j, ip in enumerate(ips):
                for k, port in enumerate(ports):
                    servers.append(dict())
                    servers[-1]['remarks'] = 'NoBey {}-{}-{}'.format(name, j, k)
                    (
                        servers[-1]['server'],
                        servers[-1]['password'],
                        servers[-1]['server_port'],
                        servers[-1]['method']) = (ip, password, port, method)

    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info
