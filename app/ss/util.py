from pyzbar.pyzbar import decode
from app.ss.config import HEADERS
import requests
import time
import threading
from app.ss import ss_local
import re
import base64
import urllib
import json
import logging


def test_connection(url='http://ip.cn', headers={'User-Agent': 'cURL'}, proxies=None, port=1080, timeout=10):
    if not proxies:
        proxies = {'http': 'socks5://localhost:{}'.format(port),
                   'https': 'socks5://localhost:{}'.format(port)}
    ok = False
    content = ''
    try:
        respond = requests.get(url, headers=headers, proxies=proxies, timeout=timeout)
        ok = respond.ok
        content = respond.text
    except Exception as e:
        print(e)
    return ok, content


def test_socks_server(dictionary=None, str_json=None, port=2001):
    try:
        try:
            loop, tcps, udps = ss_local.main(dictionary=dictionary, str_json=str_json, port=port)
        except Exception as e:
            print(e)
            return -1, 'SSR start failed'
        try:
            t = threading.Thread(target=loop.run)
            t.start()
            time.sleep(3)
            conn, content = test_connection(port=port)
            loop.stop()
            t.join()
            tcps.close(next_tick=True)
            udps.close(next_tick=True)
            time.sleep(1)
            return conn, content
        except Exception as e:
            print(e)
            return -2, 'Thread or Connection to website failed'
    except SystemExit as e:
        return e.code - 10, 'Unknown failure'


def validate(websites):
    for servers in websites:
        print(servers['info'])
        for server in servers['data']:
            result, info = test_socks_server(str_json=server['json'])
            print('>' * 10, '结果:', result)
            if result is True:
                print('>' * 10, '测试通过！')
            elif result == -1:
                print(server['json'])
            server['status'] = result
            server['content'] = info
    return websites




def parse_uri(uri, default_title='untitled'):
    """
    将ssr://或者ss:/链接解码为服务器信息
    :param uri:
    :param default_title:
    :return:
    """
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


def get_href(string, pattern='.*'):
    found = re.findall('(?<=<a\s+href=")[^"]+(?=">%s</a>)' % pattern, string)
    if found:
        return found[0]


if __name__ == '__main__':
    dates = qr_decode('http://my.freess.org/images/servers/jp01.png')
    print(dates)