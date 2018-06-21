#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本代码使用了 regex beautifulsoup4 这些第三方库，
只支持Python3以上的版本，在Linux下写成，请读者自行安装这三个第三方库，
如果遇到任何运行问题请联系我。
如果觉得这个脚本帮到了你，不妨为我的GitHub项目加个星呗～
"""
import regex as re
from bs4 import BeautifulSoup
import logging
import requests
from app.ss.parse import parse, scanNetQR, gen_uri
from app.ss.ssr_check import validate
from app.ss.tools import cf_request, load_headless_webdriver


__author__ = 'Charles Xu'
__email__ = 'charl3s.xu@gmail.com'
__my_girlfriend__ = '小胖儿～'


fake_ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}


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
                servers.append(parse(server, ' '.join([title, name, str(i)])))
            except Exception as e:
                logging.exception(e, stack_info=False)
                print('URL:', url, 'SERVER', server)
    except Exception as e:
        print(url)
        logging.exception(e, stack_info=False)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info


def crawl_freess_cx(url='https://ss.freess.org', headers=fake_ua):
    print('req fscx...')
    servers = list()
    try:
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'html.parser')
        title = soup.find('title').text
        msg = soup.find('section', attrs={'id': 'banner'}).text.strip()

        info = {'message': msg, 'url': url, 'name': str(title)}
        qr = list(map(lambda x: x.find('a').get('href'), soup.find_all('div', attrs={'class': '4u 12u(mobile)'})))
        for i, img_url in enumerate(qr):
            try:
                servers.append(parse(scanNetQR(img_url, headers=headers), ' '.join([title, str(i)])))
            except Exception as e:
                logging.exception(e, stack_info=False)
                print('IMG_URL FOR freess.cx:', img_url)
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info


def crawl_yitianjian(url='https://free.yitianjianss.com', headers=fake_ua):
    print('req yitianjian...')
    servers = list()
    try:
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'html.parser')
        title = 'yitianjianss'
        info = {'message': '为确保安全，服务器地址会不定期更新。', 'url': url, 'name': str(title)}
        qr = map(lambda x: url + x.attrs['src'], soup.find_all('img'))
        for i, img_url in enumerate(qr):
            try:
                servers.append(parse(scanNetQR(img_url, headers=headers), ' '.join([title, str(i)])))
            except Exception as e:
                logging.exception(e, stack_info=False)
                print('IMG_URL FOR yitianjianss:', img_url)
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info


def acquire_doub_url(url='https://doub.io/sszhfx/'):
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


def crawl_iss(url='https://my.ishadowx.net', headers=fake_ua):
    print('req iss...')

    try:
        data = requests.get(url, headers=headers)
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
        all_server_data = soup.find_all('div', attrs={'class': 'hover-text'})
        servers = list()
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}

    for i, server in enumerate(all_server_data):
        try:
            servers.append(dict())
            server_data = re.split('\s*\n\s*', server.text.strip())
            servers[-1]['server'] = server_data[0].split(':')[-1].strip()
            servers[-1]['server_port'] = re.findall('\d+', server_data[1])[0]
            servers[-1]['remarks'] = ' '.join(['ishadowx.com', str(i)])
            servers[-1]['password'] = server_data[2].split(':')[-1].strip()
            servers[-1]['method'] = server_data[3].split(':')[-1].strip()
            if 'QR' not in server_data[4]:
                servers[-1]['ssr_protocol'], servers[-1]['obfs'] = server_data[4].strip().split(maxsplit=1)
                servers[-1]['remarks'] = ' '.join([servers[-1]['remarks'], 'SSR'])
        except Exception as e:
            logging.exception(e, stack_info=True)
    return servers, info


def __crawl_free_ss_site(url='https://free-ss.site', headers=fake_ua):
    # NOT FINISHED YET, DO NOT KNOW WHY CANNOT GET THIS PAGE CORRECTLY
    headless_webdriver = load_headless_webdriver()
    try:
        headless_webdriver.get(url)
        source = headless_webdriver.page_source
    finally:
        headless_webdriver.quit()


def _crawl_free_ss_site(url='https://free-ss.site/ss.json', headers=fake_ua):
    print('req free_ss_site/ss.json...')
    info = {'message': '部分账号大概每隔6小时变1次', 'name': '免费上网帐号', 'url': 'https://free-ss.site/'}
    try:
        respond = cf_request(url, headers=headers)
        data = respond.json()['data']
        servers = list(map(lambda x: {
                       'remarks': x[6],
                       'server': x[1],
                       'server_port': x[2],
                       'password': x[3],
                       'method': x[4]
                       }, data))
    except Exception as e:
        logging.exception(e, stack_info=True)
        print(respond.text)
        print('-' * 30)
    return servers, info


def main(debug=list()):

    result = list()
    # Specified functions for requesting servers
    websites = [globals()[i] for i in filter(lambda x: x.startswith('crawl_'), globals())]
    from app.config import url

    websites.extend([(i, None) for i in url])
    websites.extend([(i, fake_ua, i[-1]) for i in acquire_doub_url()])

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
