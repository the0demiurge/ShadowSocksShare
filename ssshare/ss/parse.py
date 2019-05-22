#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import zbar
import requests
from PIL import Image
from io import BytesIO
from numpy import array, uint8
import base64
import urllib
import json
import logging


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
        bytes(str(decoded), 'utf-8')).decode('utf-8').replace('=', '')


def parse(uri, default_title='untitled'):
    server = dict()
    stripped = re.sub('ssr?://', '', uri)
    if uri[2] == ':':
        # ss
        if '#' in uri:
            stripped, remarks = stripped.split('#')[:2]
            server['remarks'] = urllib.parse.unquote(remarks)
        else:
            server['remarks'] = default_title
        decoded = decode(stripped)
        data = decoded.split('@', maxsplit=1)
        server['method'], server['password'] = data[0].split(':', maxsplit=1)
        server['server'], server['server_port'] = data[1].rsplit(':', maxsplit=1)
    elif uri[2] == 'r':
        # ssr
        decoded = decode(stripped)
        data = decoded.split('/?')
        [
            server['server'],
            server['server_port'],
            server['ssr_protocol'],
            server['method'],
            server['obfs'],
            password_enc,
        ] = data[0].rsplit(':', maxsplit=5)
        server['password'] = decode(password_enc)
        server['remarks'] = default_title
        if len(data) > 1:
            appendix = data[1].split('&')
            content = {i.split('=')[0]: i.split('=')[1] for i in appendix}
            for key in content:
                server[key] = decode(content[key])
        if server['ssr_protocol'] != 'origin' and server['obfs'] != 'plain':
            server['remarks'] += ' SSR'
    return server


def scanNetQR(img_url, headers=None):

    if img_url.startswith('http'):
        img_bytes = requests.get(img_url, headers=headers).content
    elif img_url.startswith('data:image'):
        img_bytes = base64.decodebytes(bytes(img_url.split(',')[1], 'utf-8'))
    img = array(Image.open(BytesIO(img_bytes)))
    info = scanner.scan(img.astype(uint8) * 255) + scanner.scan((1 - img).astype(uint8) * 255)
    if len(info) == 0:
        raise ValueError('scanner fail to identify qr code')
    return info[0].data.decode('utf-8')


def get_href(string, pattern='.*'):
    found = re.findall(r'(?<=<a\s+href=")[^"]+(?=">%s</a>)' % pattern, string)
    if found:
        return found[0]


def gen_uri(servers):
    '''{
                "server": server['server'],
                "server_ipv6": "::",
                "server_port": int(server['server_port']),
                "local_address": "127.0.0.1",
                "local_port": 1080,
                "password": server['password'],
                "timeout": 300,
                "udp_timeout": 60,
                "method": method,
                "protocol": ssr_protocol,
                "protocol_param": "",
                "obfs": obfs,
                "obfs_param": "",
                "fast_open": False,
                "workers": 1,
                "group": "ss.pythonic.life"
            },'''

    result_servers = list()
    for server in servers:
        if 'password' not in server:
            server['password'] = ''
        try:
            for key in ['method', 'password', 'server', 'server_port']:
                assert key in server, '{key} not in server data'.format(key)
            for k, v in (('ssr_protocol', 'origin'), ('obfs', 'plain')):
                if k in server and server[k] == v:
                    server.pop(k)

            is_ss = 'ssr_protocol' not in server and 'obfs' not in server

            if is_ss:
                # if not completed, it's ss
                decoded = '{method}:{password}@{hostname}:{port}'.format(
                    method=server['method'],
                    password=server['password'],
                    hostname=server['server'],
                    port=server['server_port'],
                )
                ss_uri = 'ss://{}#{}'.format(
                    str(base64.urlsafe_b64encode(bytes(decoded, encoding='utf8')), encoding='utf-8'),
                    urllib.parse.quote(server['remarks'])
                )

                # ssr formatted account info
                ssr_decoded = ':'.join([
                    server['server'],
                    server['server_port'],
                    'origin',
                    server['method'],
                    'plain',
                    encode(server['password']),
                ])
                ssr_decoded += '/?remarks={remarks}&group={group}'.format(
                    remarks=encode(server['remarks']),
                    group=encode("Charles Xu"),
                )

                ssr_uri = 'ssr://{endoced}'.format(
                    endoced=encode(ssr_decoded)
                )
            else:

                decoded_head = ':'.join([str(i) for i in [
                    server['server'],
                    server['server_port'],
                    server.get('ssr_protocol', 'origin'),
                    server['method'],
                    server.get('obfs', 'plain'),
                    encode(server['password'])
                ]])
                appendix = [(key, server[key]) for key in ['obfsparam', 'protoparam', 'remarks'] if key in server]
                appendix.append(('group', 'Charles Xu'))
                appendix_str = '&'.join(['{key}={val}'.format(
                    key=item[0],
                    val=encode(item[1])
                ) for item in appendix])
                decoded = '/?'.join([decoded_head, appendix_str])

                ss_uri = 'ssr://{endoced}'.format(endoced=encode(decoded))
                ssr_uri = ss_uri

            server['uri'] = ss_uri
            server['ssr_uri'] = ssr_uri
            server['decoded_url'] = urllib.parse.unquote(ss_uri)

            server_data_to_json = {
                "server": server['server'],
                "server_ipv6": "::",
                "server_port": int(server['server_port']),
                "local_address": "127.0.0.1",
                "local_port": 1080,
                "password": server['password'],
                "group": "Charles Xu"
            }
            if 'ssr_protocol' in server:
                server['protocol'] = server['ssr_protocol']
            for key in ['obfs', 'method', 'protocol', 'obfsparam', 'protoparam', 'udpport', 'uot']:
                if key in server:
                    server_data_to_json[key] = server.get(key)

            server['json'] = json.dumps(
                server_data_to_json,
                ensure_ascii=False,
                indent=2,
            )
            result_servers.append(server)
        except (KeyError, EOFError, ValueError) as e:
            logging.exception(e, stack_info=True)

    return result_servers
