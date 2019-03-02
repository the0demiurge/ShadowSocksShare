#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本代码使用了 regex beautifulsoup4 这些第三方库，
只支持Python3以上的版本，在Linux下写成，请读者自行安装这三个第三方库，
如果遇到任何运行问题请联系我。
如果觉得这个脚本帮到了你，不妨为我的GitHub项目加个星呗～
"""
from ast import literal_eval
import logging
import regex as re
import requests
import cfscrape
import js2py
from bs4 import BeautifulSoup
from app.ss.parse import parse, scanNetQR, gen_uri
from app.ss.ssr_check import validate

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


def crawl_free_ss_site(url='https://free-ss.site/', headers=fake_ua):
    print('req free_ss_site/...')
    info = {'message': '', 'name': '免费上网帐号', 'url': 'https://free-ss.site/'}
    try:
        fake_ua = headers

        sess = cfscrape.create_scraper()

        encc_url = url + 'ajax/libs/encc/0.0.0/encc.min.js'
        crypto_url = url + 'ajax/libs/crypto-js/3.1.9-1/crypto-js.min.js'

        headers = {'Referer': url, 'Origin': url}
        headers.update(fake_ua)

        html = sess.get(url, headers=fake_ua).text
        print('html')
        encc_js = sess.get(encc_url, headers=headers).text
        print('encc')
        crypto_js = sess.get(crypto_url, headers=headers).text
        print('crypto')

        soup = BeautifulSoup(html, 'lxml')
        script = next(filter(lambda x: 'src' not in x.attrs, soup.findAll('script'))).contents[0]

        def get_value(char):
            value_exp = re.findall(r'(?<=var)\s+{char}\s*=\s*[^;]+(?=;)'.format(char=char), script)[1]
            return literal_eval(value_exp.split('=')[1])

        value_dict = {
            'a': get_value('a'),
            'b': get_value('b'),
            'c': get_value('c'),
        }

        value_dict['c'] = js2py.eval_js(encc_js + 'encc("{c}");'.format(c=value_dict['c']))
        replace_char = re.findall(r'(?<=function\()\w(?=\)\{\s*\$.post\()', script, flags=re.MULTILINE)[0]
        img = re.findall(r"(?<=decodeImage\(')data:image[^']+(?=')", script)[0]
        value_dict[replace_char] = scanNetQR(img)

        d = sess.post(
            url + "data.php",
            headers=headers,
            data={
                'a': value_dict['a'],
                'b': value_dict['b'],
                'c': value_dict['c']
            }).text
        print('d')

        assert len(d) > 0, 'request for encrypted data failed'

        variables = ';var a = "{a}";var d = "{d}";var b = "{b}"'.format(
            a=value_dict['a'],
            b=value_dict['b'],
            d=d
        )
        xy = ';var x=CryptoJS.enc.Latin1.parse(a);var y=CryptoJS.enc.Latin1.parse(b);'
        ev = js2py.eval_js(re.findall(r'(?<=eval)\(function.*', script)[1]) + 'dec.toString(CryptoJS.enc.Utf8);'

        json_data = js2py.eval_js(crypto_js + variables + xy + ev)
        try:
            data = json.loads(json_data)
            data = data['data'][0]
        except Exception as e:
            print(json_data)

        servers = [{
            'remarks': x[6],
            'server': x[1],
            'server_port': x[2],
            'password': x[4],
            'method': x[3]
        } for x in data]
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
