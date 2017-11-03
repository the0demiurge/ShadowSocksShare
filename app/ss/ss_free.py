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
import logging
import requests
import base64
import json
from app.ss.parse import parse, scanNetQR
from app.ss.ssr_check import validate


__author__ = 'Charles Xu'
__email__ = 'charl3s.xu@gmail.com'
__my_girlfriend__ = '小胖儿～'


fake_ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'}


def get_href(string, pattern='.*'):
    found = re.findall('(?<=<a\s+href=")[^"]+(?=">%s</a>)' % pattern, string)
    if found:
        return found[0]


def request_url(url, headers=None, name=''):
    print('req', url)

    data = set()
    servers = list()
    try:
        response = requests.get(url, headers=headers, verify=False).text
        data.update(map(lambda x: re.sub('\s', '', x), re.findall('ssr?://[a-zA-Z0-9=]+', response)))
        soup = BeautifulSoup(response, 'html.parser')
        title = soup.find('title').text

        info = {'message': '', 'url': url, 'name': str(title)}
        for i, server in enumerate(data):
            try:
                servers.append(parse(server, ' '.join([title, name, str(i)])))
            except Exception as e:
                logging.exception(e, stack_info=False)
                print('URL:', url, 'SERVER', server)
    except Exception as e:
        print(url)
        logging.exception(e, stack_info=False)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info


def request_freess_cx(url='https://freess.cx/', headers=None):
    print('req fscx...')
    qr = list()
    servers = list()
    try:
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'html.parser')
        title = soup.find('title').text
        msg = soup.find('section', attrs={'id': 'banner'}).text.strip()

        info = {'message': msg, 'url': url, 'name': str(title)}
        qr = list(map(lambda x: url.strip('/') + '/' + x.find('a').get('href'), soup.find_all('div', attrs={'class': '4u 12u(mobile)'})))
        for i, img_url in enumerate(qr):
            print('req img', img_url)
            try:
                servers.append(parse(scanNetQR(img_url), ' '.join([title, str(i)])))
            except Exception as e:
                print(img_url)
                logging.exception(e, stack_info=False)
                print('IMG_URL FOR freess.cx:', img_url)
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info


def request_doub_url(url='https://doub.io/sszhfx/'):
    print('req doub...')

    try:
        html = requests.get(url, headers=fake_ua)
        soup = BeautifulSoup(html.text, 'html.parser')
        urls = list(set(map(lambda x: x.get('href'), filter(
            lambda x: x.text.strip() != '1', soup.find_all('a', attrs={'class': 'page-numbers'})))))
        urls.append(url)
    except Exception as e:
        logging.exception(e, stack_info=True)
        print('DOUB_URL:', url)
        urls = [url]
    return set(urls)


def request_iss(url='http://ss.ishadowx.com/'):
    print('req iss...')

    try:
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}

    try:

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
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}

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
        except Exception as e:
            logging.exception(e, stack_info=True)
    return servers, info


def request_5752me(url='https://wget.5752.me/Computer/soft/socks5%E4%BB%A3%E7%90%86/%E5%85%8D%E8%B4%B9ss%E8%B4%A6%E5%8F%B7.html'):
    print('req 5752...')
    servers = list()
    try:
        data = requests.get(url)
        if 'IP地址' in data.content.decode('gb2312'):
            data = data.content.decode('gb2312')
        elif 'IP地址' in data.text:
            data = data.text
        else:
            raise Exception('没找到5752信息：' + url)
        info = {'message': '', 'name': '自得其乐', 'url': 'https://www.5752.me/'}
        data = data.split('<br/>')

        avail_data = list(filter(lambda x: 'IP地址' in x, data))
        if len(avail_data) == 0:
            raise Exception('5752里面资料大概改变形式了' + '\n'.join(data))

        for i, server in enumerate(avail_data):
            servers.append(dict())
            servers[-1]['remarks'] = '自得其乐 {}'.format(i)
            (
                servers[-1]['server'],
                servers[-1]['password'],
                servers[-1]['server_port'],
                servers[-1]['method']) = server.split()[1::2]

    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
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


def request_xiaoshuang(url='https://xsjs.yhyhd.org/free-ss'):
    print('req xcud...')
    try:
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
        data = soup.find('div', attrs={'id': 'ss-body'})
        data = data.text.strip().split('\n\n\n')
        info = {'message': data[0].split('\n')[0], 'name': '小双加速', 'url': url}
        data[0] = data[0].split('\n', maxsplit=1)[-1]
        servers = list()
        for server in data:
            server_data = server.strip().split('\n')
            servers.append(dict())
            servers[-1]['remarks'] = '小双{}'.format(server_data[0]).strip()
            servers[-1]['server'] = server_data[1].split()[1].strip()
            servers[-1]['server_port'] = server_data[1].split()[3].strip()
            servers[-1]['password'] = server_data[2].split()[3].strip()
            servers[-1]['method'] = server_data[2].split()[1].strip()
            servers[-1]['ssr_protocol'] = server_data[3].split()[1].split(':')[1].strip()
            servers[-1]['obfs'] = server_data[3].split()[2].split(':')[1].strip()
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info

# this cannot use for now


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
    def encode(decoded):
        return base64.urlsafe_b64encode(bytes(decoded, 'utf-8')).decode('utf-8').replace('=', '')

    def decode(string):
        return str(base64.urlsafe_b64decode(bytes(string + (4 - len(string) % 4) * '=', 'utf-8')), 'utf-8')

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
            for key in ['obfs', 'method', 'ssr_protocol', 'obfsparam', 'protoparam']:
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


def main(debug=list()):
    result = list()

    # Specified functions for requesting servers
    websites = [
        request_iss,
        request_freess_cx,
        request_nobey,
        request_5752me,
    ]
    from app.config import url

    websites.extend([(i, None) for i in url])
    websites.extend([(i, fake_ua, i[-1]) for i in request_doub_url()])

    for website in websites:
        try:
            if type(website) is tuple:
                data, info = request_url(*website)
            else:
                data, info = website()
            result.append({'data': gen_uri(data), 'info': info})
        except Exception as e:
            logging.exception(e, stack_info=False)
            print('Error in', website, type(website))

    # check ssr configs
    if 'no_validate' in debug:
        validated_servers = result
    else:
        validated_servers = validate(result)
    # remove useless data
    servers = list(filter(lambda x: len(x['data']) > 0, validated_servers))
    print('-' * 10, '数据获取完毕', '-' * 10)
    return servers


if __name__ == '__main__':
    print(main())
