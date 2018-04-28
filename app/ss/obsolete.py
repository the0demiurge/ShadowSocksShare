#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Storing sites or functions that not working anymore... maybe"""
from bs4 import BeautifulSoup
import requests
import logging
import regex as re








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
