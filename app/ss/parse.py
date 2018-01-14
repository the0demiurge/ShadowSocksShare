#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import zbar
import requests
from PIL import Image
from io import BytesIO
from numpy import array, uint8
import base64


scanner = zbar.Scanner()


def decode(string):
    try:
        return str(
            base64.urlsafe_b64decode(
                bytes(
                    string.strip('/') + (4 - len(string.strip('/')) % 4) * '=' + '====',
                    'utf-8')), 'utf-8')
    except Exception as e:
        print(e, string)
        raise Exception(e, string)


def encode(decoded):
    return base64.urlsafe_b64encode(
        bytes(decoded, 'utf-8')).decode('utf-8').replace('=', '')


def reverse_str(string):
    return ''.join(list(reversed(string.strip()))).strip()


def parse(uri, default_title='untitled'):
    server = dict()
    stripped = re.sub('ssr?://', '', uri)
    if uri[2] is ':':
        # ss
        if '#' in uri:
            stripped, server['remarks'] = stripped.split('#')[:2]
        else:
            server['remarks'] = default_title
        decoded = decode(stripped)
        data = list(map(
            reverse_str,
            reverse_str(decoded).split('@', maxsplit=1)))
        server['method'], server['password'] = data[1].split(':', maxsplit=1)
        server['server_port'], server['server'] = map(
            reverse_str,
            reverse_str(data[0]).split(':', maxsplit=1))
    elif uri[2] is 'r':
        # ssr
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


uri = 'https://freess.cx/images/servers/jp01.png'


def scanNetQR(img_url, headers=None):
    img = array(Image.open(BytesIO(requests.get(img_url, headers=headers).content)))
    return scanner.scan(img.astype(uint8) * 255)[0].data.decode('utf-8')
