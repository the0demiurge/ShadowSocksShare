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
            content = {i.split('=')[0]: i.split('=')[1] for i in data}
            for key in content:
                if key in ['remarks', 'group']:
                    server[key] = decode(content[key])
                else:
                    server[key] = content[key]
        server['remarks'] += ' SSR'
    return server


uri = 'https://freess.cx/images/servers/jp01.png'


def scanNetQR(img_url, headers=None):
    img = array(Image.open(BytesIO(requests.get(img_url, headers=headers).content)))
    return scanner.scan(img.astype(uint8) * 255)[0].data.decode('utf-8')


def get_href(string, pattern='.*'):
    found = re.findall('(?<=<a\s+href=")[^"]+(?=">%s</a>)' % pattern, string)
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
            try:
                # SSR信息是否完整
                decoded = ':'.join([
                                   server['server'],
                                   server['server_port'],
                                   server['ssr_protocol'],
                                   server['method'],
                                   server['obfs'],
                                   encode(server['password'])
                                   ])
                decoded += '/?remarks={remarks}&group={group}'.format(
                    remarks=encode(server['remarks']),
                    group=encode("Charles Xu"))

                ss_uri = 'ssr://{endoced}'.format(
                    endoced=encode(decoded))
                ssr_uri = ss_uri

            except (KeyError, EOFError):
                # 不完整则是SS
                decoded = '{method}:{password}@{hostname}:{port}'.format(
                    method=server['method'],
                    password=server['password'],
                    hostname=server['server'],
                    port=server['server_port'],
                )
                ss_uri = 'ss://{}#{}'.format(
                    str(base64.urlsafe_b64encode(bytes(decoded, encoding='utf8')), encoding='utf-8'),
                    urllib.parse.quote(server['remarks']))

                # ssr格式的ss帐号信息
                ssr_decoded = ':'.join([
                    server['server'],
                    server['server_port'],
                    'origin',
                    server['method'],
                    'plain',
                    encode(server['password'])
                ])
                ssr_decoded += '/?remarks={remarks}&group={group}'.format(
                    remarks=encode(server['remarks']),
                    group=encode("Charles Xu"))

                ssr_uri = 'ssr://{endoced}'.format(
                    endoced=encode(ssr_decoded))

            server['uri'] = ss_uri
            server['ssr_uri'] = ssr_uri
            # print(ssr_uri, decode(ssr_uri[6:]))
            server['decoded_url'] = urllib.parse.unquote(ss_uri)

            server_data_to_json = {
                "server": server['server'],
                "server_ipv6": "::",
                "server_port": int(server['server_port']),
                "local_address": "127.0.0.1",
                "local_port": 1080,
                "password": server['password'],
                # "timeout": 300,
                # "udp_timeout": 60,
                # "fast_open": False,
                # "workers": 1,
                "group": "Charles Xu"
            }
            for key in ['obfs', 'method', 'ssr_protocol', 'obfsparam', 'protoparam', 'udpport', 'uot']:
                if key in server:
                    server_data_to_json[key] = server.get(key)

            server['json'] = json.dumps(server_data_to_json,
                                        ensure_ascii=False,
                                        indent=2)
            result_servers.append(server)
        except (KeyError, EOFError):
            try:
                href = get_href(server['string'], '.*查看连接信息.*')
                server['href'] = href
            except Exception as e:
                logging.exception(e, stack_info=True)
        except ValueError as e:
            logging.exception(e, stack_info=True)
    return result_servers
