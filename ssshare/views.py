#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import random
import logging
import time
import threading
import os
from ssshare import app
from ssshare.ascii import birthday_2017, ss_title
from ssshare.ss import crawler
from ssshare import donation
from flask import render_template, send_from_directory, abort
from apscheduler.schedulers.background import BackgroundScheduler


# Config for disqus comment board
DOMAIN = 'http://ss.pythonic.life'
DISQUS_IDENTIFIER = 'shadowsocksshare'


servers = [{'data': [], 'info': {'message': '别着急，正在爬数据，十分钟后再回来吧：）', 'url': 'http://ss.pythonic.life', 'name': '免费 ShadowSocks 账号分享'}}]
curtime = time.ctime()

encoded = ''
full_encoded = ''
jsons = list()
full_jsons = list()
scheduler = BackgroundScheduler()


def update_servers():
    try:
        # servers
        global servers
        servers = crawler.main()
        # subscription
        global encoded
        global full_encoded
        global jsons
        global full_jsons
        jsons = list()
        decoded = list()
        full_decoded = list()
        for website in servers:
            for server in website['data']:
                full_decoded.append(server['ssr_uri'])
                full_jsons.append(server['json'])
                if server['status'] > 0:
                    decoded.append(server['ssr_uri'])
                    jsons.append(server['json'])

        decoded = '\n'.join(decoded)
        encoded = base64.urlsafe_b64encode(bytes(decoded, 'utf-8'))
        full_decoded = '\n'.join(full_decoded)
        full_encoded = base64.urlsafe_b64encode(bytes(full_decoded, 'utf-8'))
        time.sleep(7200)
    except Exception as e:
        logging.exception(e, stack_info=True)


# counter_path = os.path.expanduser('/tmp/counter')
counter_path = 'memory'
count = 0


def counter(counter_path=counter_path, update=True):
    if update:
        if counter_path == 'memory':
            global count
            count += 1
        else:
            if not os.path.exists(os.path.split(counter_path)[0]):
                os.makedirs(os.path.split(counter_path)[0])
            if not os.path.exists(counter_path):
                open(counter_path, 'w').write('0')
            count = int(open(counter_path).readline())
            open(counter_path, 'w').write(str(count + 1))
    return count


@app.route('/')
def index():
    try:
        return render_template(
            'index.html',
            servers=servers,
            ss=ss_title[random.randint(0, len(ss_title) - 1)],
            counter=counter(),
            ctime=curtime,
            PAGE_URL=DOMAIN + '/',
            PAGE_IDENTIFIER='shadowsocksshare'
        )
    except Exception as e:
        logging.exception(e, stack_info=True)


@app.route('/full')
def full():
    try:
        return render_template(
            'full.html',
            servers=servers,
            ss=ss_title[random.randint(0, len(ss_title) - 1)],
            counter=counter(),
            ctime=curtime,
        )
    except Exception as e:
        logging.exception(e, stack_info=True)


@app.route('/<string:path>')
def pages(path):
    print(path)
    try:
        a, b = path.split('-')
        a, b = int(a), int(b)
    except Exception:
        abort(404)

    if a >= len(servers):
        abort(404)
    elif b >= len(servers[a]['data']):
        abort(404)

    try:
        uri = servers[a]['data'][b].get('decoded_url', '')
        remarks = servers[a]['data'][b].get('remarks', 'None')
        server = servers[a]['data'][b].get('server', 'None')
        server_port = servers[a]['data'][b].get('server_port', 'None')
        password = servers[a]['data'][b].get('password', 'None')
        method = servers[a]['data'][b].get('method', 'None')
        ssr_protocol = servers[a]['data'][b].get('ssr_protocol', 'None')
        obfs = servers[a]['data'][b].get('obfs', 'None')
        href = servers[a]['data'][b].get('href', 'None')
        json = servers[a]['data'][b].get('json', 'None')
        obfsparam = servers[a]['data'][b].get('obfsparam', 'None')
        protoparam = servers[a]['data'][b].get('protoparam', 'None')
        status = servers[a]['data'][b].get('status', 'None')
        content = servers[a]['data'][b].get('content', 'None')

        return render_template(
            'pages.html',
            uri=uri,
            server=server,
            server_port=server_port,
            password=password,
            method=method,
            ssr_protocol=ssr_protocol,
            obfs=obfs,
            href=href,
            remarks=remarks,
            counter=counter(),
            server_data=servers[a]['data'][b],
            json=json,
            obfsparam=obfsparam,
            protoparam=protoparam,
            status=status,
            content=content,
        )
    except Exception as e:
        logging.exception(e, stack_info=True)


@app.route('/html/<path:path>')
def static_html(path):
    try:
        return render_template(path, )
    except Exception as e:
        logging.exception(e)
        abort(404)


@app.route('/donation')
def html_donation():
    try:
        return render_template(
            'donate.html',
            data=donation.data,
            sum_people=donation.sum_people,
            sum_money=donation.sum_money,
        )
    except Exception as e:
        logging.exception(e)
        abort(404)


@app.route('/subscribe')
def subscribe():
    counter('', False)
    return encoded


@app.route('/full/subscribe')
def full_subscribe():
    counter('', False)
    return full_encoded


@app.route('/json')
def subscribe_json():
    counter('', False)
    return '{}' if len(jsons) == 0 else random.sample(jsons, 1)[0]


@app.route('/full/json')
def full_subscribe_json():
    counter('', False)
    return '{}' if len(jsons) == 0 else random.sample(full_jsons, 1)[0]


@app.route('/js/<path:path>')
def send_jsadfsadfs(path):
    return send_from_directory('js', path)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static', 'favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', ), 404


@app.route('/gift')
def gift():
    return birthday_2017


def start():
    update_thread = threading.Thread(target=update_servers)
    scheduler.add_job(update_servers, "cron", minute=random.randint(1, 15), second=random.randint(0, 59))
    update_thread.start()
    scheduler.start()
