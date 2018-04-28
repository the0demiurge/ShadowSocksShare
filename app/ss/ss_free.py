#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本代码使用了 regex beautifulsoup4 这些第三方库，
只支持Python3以上的版本，在Linux下写成，请读者自行安装这三个第三方库，
如果遇到任何运行问题请联系我。
如果觉得这个脚本帮到了你，不妨为我的GitHub项目加个星呗～
"""
import requests
from app.ss.util import  validate
from app.ss.util import universal_request_url, parse_uri, gen_uri
import logging
from bs4 import BeautifulSoup
from app.ss.config import HEADERS,LOG_FILENAME
import regex as re
import time
import logging
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode


logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.ERROR,
)

def qr_decode(url):
    """
    对网络上二维码图片进行解码
    :param url: 二维码图片的url
    :return: 成功返回解码后的字符串
    """
    try:
        if isinstance(url, str):
            ss_data = decode(Image.open(BytesIO(requests.get(url, headers=HEADERS, proxies=PROXIES).content)))
            return str(ss_data[0].data, encoding='utf-8')
    except Exception:
        logging.ERROR("二维码解码失败:" + url)
        return ''


# 有效 测试日期：2018年4月28日
@universal_request_url('https://global.ishadowx.net')
def request_iss(response):
    if response == '':
        return [], {'message': '', 'url': '', 'name': ''}
    else:
        soup = BeautifulSoup(response, 'lxml')

    try:

        info = {
            'message': soup.find('div', attrs={'id': 'portfolio'}).find('div', attrs={'class': 'section-title text-center center'}).text,
            'name': 'ishadowx',
            'url': 'https://global.ishadowx.net'}

        '''servers[-1]['name'] = tmp[0]
        servers[-1]['server'] = tmp[0]
        servers[-1]['server_port'] = tmp[0]
        servers[-1]['password'] = tmp[0]
        servers[-1]['method'] = tmp[0]
        servers[-1]['ssr_protocol'] = tmp[0]
        servers[-1]['obfs'] = tmp[0]'''

        server_data = soup.find_all('div', attrs={'class': 'hover-text'})
        servers = list()
    except Exception as e:
        logging.ERROR(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}

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
    return servers, info


# 有效 测试日期：2018年4月28日
@universal_request_url('http://my.freess.org/')
def request_freess_cx(response):
    servers = []
    names = []
    suffixs = ['jp01.png', 'jp02.png', 'jp03.png', 'us01.png', 'us02.png', 'us03.png']
    qr_urls = ['http://my.freess.org/images/servers/' + suffix for suffix in suffixs]
    try:
        soup = BeautifulSoup(response, 'lxml')
        for title in soup.find_all('div', class_="4u 12u(mobile)"):
            soup = BeautifulSoup(str(title), 'lxml')
            names.append(soup.get_text())
        info = {'message': '', 'url': qr_urls, 'name': names}
        for i in range(6):
            ss_list = qr_decode(qr_urls[i])
            servers.append(parse_uri(ss_list, names[i]))
            time.sleep(3)
    except Exception:
        logging.ERROR('请求出错: ' + 'http://my.freess.org/')
    finally:
        return servers, info


# 有效 测试日期： 2018年4月28日
@universal_request_url('https://raw.githubusercontent.com/fq1234/home/master/README.md')
def request_fq123(response):
    if response:
        servers = [{
            'remarks': 'fq123.tk',
            'server': '198.199.66.220',
            'server_port': '4001',
            'password': 'CHANGCHENG',
            'method': 'rc4-md5',
        }]
        info = {'message': '', 'name': 'fq123', 'url': 'http://fq123.tk/'}
    else:
        return [], {'message': 'no response', 'url': '', 'name': ''}
    return servers, info

# 有效 测试日期： 2018年4月28日
# @universal_request_url('https://doub.io/sszhfx/')
# def request_doub_url(response):
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

# def request_newpac(url='https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7'):
#     data = requests.get(url)
#     soup = BeautifulSoup(data.text, 'html.parser')
#
#     ss_list = list()
#
#     for i in soup.find_all('p'):
#         if re.match('\<p\>\s*服务器\d+[^:：]*[:：]', str(i)):
#             ss_list.append(str(i))
#
#     servers = list()
#     for i in ss_list:
#         servers.append(dict())
#         servers[-1]['string'] = i
#         # name
#         tmp = re.findall('服务器\d+[^:：]*(?=\s*[:：])', i)
#         if tmp:
#             servers[-1]['remarks'] = tmp[0]
#
#         # server
#         tmp = re.findall('(?<=服务器\s*\d+[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[\w\d\.]+', i)
#         if tmp:
#             servers[-1]['server'] = tmp[0]
#
#         # server_port
#         tmp = re.findall('(?<=端口\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)\d+', i)
#         if tmp:
#             servers[-1]['server_port'] = tmp[0]
#
#         # password
#         tmp = re.findall('(?<=密码\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
#         if tmp:
#             servers[-1]['password'] = tmp[0]
#
#         # method
#         tmp = re.findall('(?<=加密方[式法]\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
#         if tmp:
#             servers[-1]['method'] = tmp[0]
#
#         # SSR协议
#         tmp = re.findall('(?<=SSR协议\s*[^:：]*[:：]\s*[^a-zA-Z_0-9]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
#         if tmp:
#             servers[-1]['ssr_protocol'] = tmp[0]
#
#         # 混淆
#         tmp = re.findall('(?<=混淆\s*[^:：]*[:：]\s*[^a-zA-Z0-9_]*)[a-zA-Z\d\.\+\-_\*\\/]+', i)
#         if tmp:
#             servers[-1]['obfs'] = tmp[0]
#     info = {'message': '', 'name': 'new-pac', 'url': url}
#     return servers, info


def request_url(url, headers=None, name=''):
    print('req', url)

    data = set()
    servers = list()
    try:
        response = requests.get(url, headers=headers, verify=False).text
        data.update(map(lambda x: re.sub('\s', '', x), re.findall('ssr?://[a-zA-Z0-9_]+=*', response)))
        soup = BeautifulSoup(response, 'html.parser')
        title = soup.find('title').text

        info = {'message': '', 'url': url, 'name': str(title)}
        for i, server in enumerate(data):
            try:
                servers.append(parse_uri(server, ' '.join([title, name, str(i)])))
            except Exception as e:
                logging.exception(e, stack_info=False)
                print('URL:', url, 'SERVER', server)
    except Exception as e:
        print(url)
        logging.exception(e, stack_info=False)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info







# 函数字典
# url:url爬虫函数名



def main(debug=list()):
    result = list()
    validated_servers = list()
    # Specified functions for requesting servers
    websites = [
        request_iss,
        request_freess_cx,
        request_fq123,
    ]
    from app.ss.config import url
    websites.extend([(i, None) for i in url])
    # websites.extend([(i, HEADERS, i[-1]) for i in request_doub_url()])
    for website in websites:
        try:
            if type(website) is tuple:
                data, info = request_url(*website)
            else:
                data, info = website()
            result.append({'data': gen_uri(data), 'info': info})
        except Exception:
            logging.ERROR('Error in', website, type(website))

    # check ssr configs
    # try:
    #     if 'no_validate' in debug:
    #         validated_servers = result
    #     else:
    #         validated_servers = validate(result)
    # except Exception:
    #     logging.ERROR('Cannot validate the ')
    validated_servers = result

    # remove useless data
    servers = list(filter(lambda x: len(x['data']) > 0, validated_servers))
    print('-' * 10, '数据获取完毕', '-' * 10)
    return servers


if __name__ == '__main__':
    print(main())
