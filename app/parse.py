#!/usr/bin/env python
# -*- utf-8 -*-
import re
import base64


def decode(string):
    return str(base64.urlsafe_b64decode(bytes(string + (4 - len(string) % 4) * '=', 'utf-8')), 'utf-8')


def encode(decoded):
    return base64.urlsafe_b64encode(bytes(decoded, 'utf-8')).decode('utf-8').replace('=', '')


def parse(uri):
    server = dict()
    stripped = re.sub('ssr?://', '', uri)
    if uri[2] is ':':
        if '#' in uri:
            stripped, server['remarks'] = stripped.split('#')[:2]
        else:
            server['remarks'] = 'untitled'
        decoded = decode(stripped)
        data = decoded.split('@')
        server['method'], server['password'] = data[0].split(':')
        server['server'], server['server_port'] = data[1].split(':')
    elif uri[2] is 'r':
        decoded = decode(stripped)
        if '/?' in decoded:
            data = decoded.split('/?')
        else:
            data = [decoded]
        [
            server['server'],
            server['server_port'],
            server['ssr_protocol'],
            server['method'],
            server['obfs']] = data[0].split(':')[:5]
        server['password'] = decode(data[0].split(':')[5])
        server['remarks'] = 'untitled'
        if len(data) > 1:
            data = data[1].split('&')
            content = {i.split('=')[0]: decode(i.split('=')[1]) for i in data}
            for key in content:
                server[key] = content[key]
        server['remarks'] += ' SSR'
    return server
