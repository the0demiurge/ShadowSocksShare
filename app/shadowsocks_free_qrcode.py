#!/usr/bin/env python
# -*- utf-8 -*-
"""
本代码使用了 regex beautifulsoup4 这些第三方库，
只支持Python3以上的版本，在Linux下写成，请读者自行安装这三个第三方库，
如果遇到任何运行问题请联系我。
如果觉得这个脚本帮到了你，不妨为我的GitHub项目加个星呗～
"""
try:
    import regex as re
    from bs4 import BeautifulSoup
except ImportError:
    print('''Python缺少依赖库，请使用 pip install -U regex beautifulsoup4 或者其他方式安装此依赖。
          本软件在Linux下写成，Python版本为3.5，如果遇到任何错误，请到GitHub上提交Issue。\n''')
    exit(0)

import urllib
# import sys
import requests
import base64
import json
from app.parse import parse
from app.config import url


__author__ = 'Charles Xu'
__email__ = 'charl3s.xu@gmail.com'
__my_girlfriend__ = '小胖儿～'


def get_href(string, pattern='.*'):
    found = re.findall('(?<=<a\s+href=")[^"]+(?=">%s</a>)' % pattern, string)
    if found:
        return found[0]


def request_url(url):
    data = list()
    try:
        response = requests.get(url, verify=False).text
        data += re.findall('ssr?://\w+', response)
    except Exception:
        return [], {'message': '', 'url': '', 'name': ''}
    soup = BeautifulSoup(response, 'html.parser')
    title = soup.find('title').text

    info = {'message': '', 'url': url, 'name': str(title)}
    servers = [parse(server) for server in data]
    return servers, info


def request_iss(url='http://ss.ishadowx.com/'):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    info = {
        'message': soup.find('div', attrs={'id': 'portfolio'}).find('div', attrs={'class': 'section-title text-center center'}).text,
        'name': 'ishadowx',
        'url': url}

    '''servers[-1]['name'] = tmp[0]
    servers[-1]['server'] = tmp[0]
    servers[-1]['server_port'] = tmp[0]
    servers[-1]['password'] = tmp[0]
    servers[-1]['method'] = tmp[0]
    servers[-1]['ssr_protocol'] = tmp[0]
    servers[-1]['obfs'] = tmp[0]'''

    soup = BeautifulSoup(data.text, 'html.parser')
    server_data = soup.find_all('div', attrs={'class': 'hover-text'})
    servers = list()

    for i, server in enumerate(server_data):
        try:
            servers.append(dict())
            server_data = server.text.strip().split('\n')
            servers[-1]['server'] = server_data[0].split(':')[-1].strip()
            servers[-1]['server_port'] = re.findall('\d+', server_data[1])[0]
            servers[-1]['remarks'] = ' '.join(['ss.ishadowx.com', str(i)])
            servers[-1]['password'] = server_data[2].split(':')[-1].strip()
            servers[-1]['method'] = server_data[3].split(':')[-1].strip()
            if 'QR' not in server_data[4]:
                servers[-1]['ssr_protocol'], servers[-1]['obfs'] = server_data[4].strip().split(maxsplit=1)
                servers[-1]['remarks'] = ' '.join([servers[-1]['remarks'], 'SSR'])
        except Exception:
            pass
    return servers, info


def request_xiaoshuang(url='https://xsjs.yhyhd.org/free-ss'):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    data = soup.find('div', attrs={'id': 'ss-body'})
    data = data.text.strip().split('\n\n\n')
    info = {'message': data[0].split('\n')[0], 'name': '小双加速', 'url': url}
    data[0] = data[0].split('\n', maxsplit=1)[-1]
    servers = list()
    for server in data:
        server = server.split('\n')
        servers.append(dict())
        servers[-1]['remarks'] = '小双{}'.format(server[0]).strip()
        servers[-1]['server'] = server[1].split()[1].strip()
        servers[-1]['server_port'] = server[1].split()[3].strip()
        servers[-1]['password'] = server[2].split()[3].strip()
        servers[-1]['method'] = server[2].split()[1].strip()
        servers[-1]['ssr_protocol'] = server[3].split()[1].split(':')[1].strip()
        servers[-1]['obfs'] = server[3].split()[2].split(':')[1].strip()
    return servers, info


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


def get_qr_uri(servers):
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
    def encode(decoded):
        return base64.urlsafe_b64encode(bytes(decoded, 'utf-8')).decode('utf-8').replace('=', '')

    def decode(string):
        return str(base64.urlsafe_b64decode(bytes(string + (4 - len(string) % 4) * '=', 'utf-8')), 'utf-8')
    for server in servers:
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

            server['uri'] = ss_uri
            server['decoded_url'] = urllib.parse.unquote(ss_uri)

            obfs = server['obfs'] if 'obfs' in server else ''
            method = server['method'] if 'method' in server else ''
            ssr_protocol = server['ssr_protocol'] if 'ssr_protocol' in server else ''
            obfsparam = server['obfsparam'] if 'obfsparam' in server else ''
            protoparam = server['protoparam'] if 'protoparam' in server else ''

            server['json'] = json.dumps({
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
                "protocol_param": protoparam,
                "obfs": obfs,
                "obfs_param": obfsparam,
                "fast_open": False,
                "workers": 1,
                "group": "Charles Xu"
            },
                ensure_ascii=False,
                indent=2)
        except (KeyError, EOFError):
            try:
                href = get_href(server['string'], '.*查看连接信息.*')
                server['href'] = href
            except Exception:
                pass
    return servers


def main():
    # servers = request_newpac()
    # servers = get_qr_uri(servers)
    # return servers
    servers_iss, info_iss = request_iss()
    servers_xiaoshuang, info_xiaoshuang = request_xiaoshuang()

    result = [
        {'data': get_qr_uri(servers_iss), 'info': info_iss},
        {'data': get_qr_uri(servers_xiaoshuang), 'info': info_xiaoshuang},
    ]
    for i in url:
        data, info = request_url(i)
        result.append({'data': get_qr_uri(data), 'info': info})
    return result


if __name__ == '__main__':
    print(main())
