#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本代码使用了 regex beautifulsoup4 这些第三方库，
只支持Python3以上的版本，在Linux下写成，请读者自行安装这三个第三方库，
如果遇到任何运行问题请联系我。
如果觉得这个脚本帮到了你，不妨为我的GitHub项目加个星呗～
"""
try:
    import regex as re
    from bs4 import BeautifulSoup
    import logging
    import requests
    from app.ss.parse import parse, scanNetQR, gen_uri
    from app.ss.ssr_check import validate
    from app.ss.tools import cf_request
except ImportError:
    print('You should install python modules following requirements.txt')
    exit(0)


__author__ = 'Charles Xu'
__email__ = 'charl3s.xu@gmail.com'
__my_girlfriend__ = '小胖儿～'


fake_ua = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}


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


def request_freess_cx(url='https://freess.cx/', headers=fake_ua):
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
                servers.append(parse(scanNetQR(img_url, headers=headers), ' '.join([title, str(i)])))
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


def request_iss(url='https://global.ishadowx.net'):
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


def request_fq123(url='https://raw.githubusercontent.com/fq1234/home/master/README.md'):
    print('req fq123...')
    try:
        data = re.split('\s*\n\s*', requests.get(url).text.split('```')[1].strip())
        servers = [{
            'remarks': 'fq123.tk',
            'server': data[0].split()[1],
            'server_port': data[1].split()[1],
            'password': data[2].split()[1],
            'method': data[3].split()[1],
        }]
        info = {'message': '', 'name': 'fq123', 'url': 'http://fq123.tk/'}
    except Exception as e:
        logging.exception(e, stack_info=True)
        return [], {'message': str(e), 'url': '', 'name': ''}
    return servers, info


def request_free_ss_site(url='https://free-ss.site/ss.json', headers=fake_ua):
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
    websites = [
        request_iss,
        request_freess_cx,
        # request_nobey,
        # request_5752me,
        request_fq123,
        request_free_ss_site,
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
