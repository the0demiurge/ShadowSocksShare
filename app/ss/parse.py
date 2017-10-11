#!/usr/bin/env python
# -*- utf-8 -*-
import re
import zbar
import requests
from imread import imread_from_blob
from numpy import uint8
import base64


scanner = zbar.Scanner()


def decode(string):
    try:
        return str(
            base64.urlsafe_b64decode(
                bytes(
                    string.strip('/') + (4 - len(string.strip('/')) % 4) * '=',
                    'utf-8')), 'utf-8')
    except Exception as e:
        print(e, string)
        raise Exception(e, string)


def encode(decoded):
    return base64.urlsafe_b64encode(
        bytes(decoded, 'utf-8')).decode('utf-8').replace('=', '')


def reverse_str(string):
    return ''.join(list(reversed(string)))


def parse(uri, default_title='untitled'):
    server = dict()
    stripped = re.sub('ssr?://', '', uri)
    if uri[2] is ':':
        if '#' in uri:
            stripped, server['remarks'] = stripped.split('#')[:2]
        else:
            server['remarks'] = default_title
        decoded = decode(stripped)
        data = decoded.split('@')
        server['method'], server['password'] = data[0].split(':')
        server['server_port'], server['server'] = map(
            reverse_str,
            reverse_str(data[1]).split(':', maxsplit=1))
    elif uri[2] is 'r':
        decoded = decode(stripped)
        if '/?' in decoded:
            data = decoded.split('/?')
        else:
            data = [decoded]
        [
            server['obfs'],
            server['method'],
            server['ssr_protocol'],
            server['server_port'],
            server['server'],
        ] = map(
            reverse_str,
            reverse_str(data[0]).split(':', maxsplit=5)[1:])
        server['password'] = decode(data[0].split(':')[-1])
        server['remarks'] = default_title
        if len(data) > 1:
            data = data[1].split('&')
            content = {i.split('=')[0]: decode(i.split('=')[1]) for i in data}
            for key in content:
                server[key] = content[key]
        server['remarks'] += ' SSR'
    return server


def scanNetQR(img_url):
    img = imread_from_blob(requests.get(img_url).content)
    return scanner.scan(img.astype(uint8) * 255)[0].data.decode('utf-8')
