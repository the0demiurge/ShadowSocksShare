#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from proxypool.util import  parse_uri, gen_uri, qr_decode, get_page
from bs4 import BeautifulSoup
from proxypool.setting import LOG_FILENAME
import regex as re
import time
import logging


logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.ERROR,
)


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        print('执行get_proxies')
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies


    # 有效 测试日期：2018年4月28日
    def crawl_iss(self):
        response = get_page('https://global.ishadowx.net')
        if response == '':
            return [], {'message': '', 'url': '', 'name': ''}
        else:
            print('获得soup')
            soup = BeautifulSoup(response, 'lxml')

        try:
            server_data = soup.find_all('div', attrs={'class': 'hover-text'})
            servers = list()
        except Exception as e:
            logging.ERROR(e, stack_info=True)
            return []

        for i, server in enumerate(server_data):
            try:
                servers.append(dict())
                server_data = re.split('\s*\n\s*', server.text.strip())
                servers[-1]['server'] = server_data[0].split(':')[-1].strip()
                servers[-1]['server_port'] = re.findall('\d+', server_data[1])[0]
                servers[-1]['remarks'] = ' '.join(['global.ishadowx.com', str(i)])
                servers[-1]['password'] = server_data[2].split(':')[-1].strip()
                servers[-1]['method'] = server_data[3].split(':')[-1].strip()
                if 'QR' not in server_data[4]:
                    servers[-1]['ssr_protocol'], servers[-1]['obfs'] = server_data[4].strip().split(maxsplit=1)
                    servers[-1]['remarks'] = ' '.join([servers[-1]['remarks'], 'SSR'])
            except Exception as e:
                logging.exception(e, stack_info=True)
        for server in servers:
            yield gen_uri(server)

    # 有效 测试日期：2018年4月28日
    def crawl_freess_cx(self):
        response = get_page('http://my.freess.org/')
        servers = []
        names = []
        suffixs = ['jp01.png', 'jp02.png', 'jp03.png', 'us01.png', 'us02.png', 'us03.png']
        qr_urls = ['http://my.freess.org/images/servers/' + suffix for suffix in suffixs]
        try:
            soup = BeautifulSoup(response, 'lxml')
            for title in soup.find_all('div', class_="4u 12u(mobile)"):
                soup = BeautifulSoup(str(title), 'lxml')
                names.append(soup.get_text())
            for i in range(6):
                ss_list = qr_decode(qr_urls[i])
                servers.append(parse_uri(ss_list, names[i]))
                time.sleep(3)
        except Exception:
            logging.ERROR('请求出错: ' + 'http://my.freess.org/')
        finally:
            for server in servers:
                yield gen_uri(server)

    # 有效 测试日期： 2018年4月28日
    def crawl_fq123(self):
        print('已获取req123')
        servers = [{
            'remarks': 'fq123.tk',
            'server': '198.199.66.220',
            'server_port': '4001',
            'password': 'CHANGCHENG',
            'method': 'rc4-md5',
        }]
        for server in servers:
            yield gen_uri(server)


    def crawl_fq124(self):
        print('已获取req124')
        servers = [{
            'remarks': 'fq123.tk',
            'server': '198.199.66.221',
            'server_port': '4001',
            'password': 'CHANGCHENG',
            'method': 'rc4-md5',
        }]
        for server in servers:
            yield gen_uri(server)


    # 有效 测试日期： 2018年4月28日
    # def request_doub_url(response):
    #     response = universal_request_url('https://doub.io/sszhfx/')
    #     urls = list()
    #     url = 'https://doub.io/sszhfx/'
    #     try:
    #         if response:
    #             soup = BeautifulSoup(response, 'lxml')
    #         else:
    #             raise Exception
    #         urls = list(set(map(lambda x: x.get('href'), filter(
    #             lambda x: x.text.strip() != '1', soup.find_all('a', attrs={'class': 'page-numbers'})))))
    #         urls.append(url)
    #     except Exception:
    #         logging.ERROR('查找逗比网址失败')
    #         urls = [url]
    #     return set(urls)



# def request_url(url, headers=None, name=''):
#     print('req', url)
#
#     data = set()
#     servers = list()
#     try:
#         response = requests.get(url, headers=headers, verify=False).text
#         data.update(map(lambda x: re.sub('\s', '', x), re.findall('ssr?://[a-zA-Z0-9_]+=*', response)))
#         soup = BeautifulSoup(response, 'html.parser')
#         title = soup.find('title').text
#
#         info = {'message': '', 'url': url, 'name': str(title)}
#         for i, server in enumerate(data):
#             try:
#                 servers.append(parse_uri(server, ' '.join([title, name, str(i)])))
#             except Exception as e:
#                 logging.exception(e, stack_info=False)
#                 print('URL:', url, 'SERVER', server)
#     except Exception as e:
#         print(url)
#         logging.exception(e, stack_info=False)
#         return [], {'message': str(e), 'url': '', 'name': ''}
#     return servers, info
# 函数字典
# url:url爬虫函数名

