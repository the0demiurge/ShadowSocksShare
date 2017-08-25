#!/usr/bin/env python
# -*- utf-8 -*-
import base64
import random
import time
import threading
import os
from app import app
from app import ss_free
from app import ss
from flask import render_template, send_from_directory, abort


servers = ss_free.main()
curtime = time.ctime()

decoded = list()
for i in servers:
    for j in i['data']:
        if j['uri'][2] is 'r':
            decoded.append(j['uri'])
decoded = '\n'.join(decoded)
encoded = base64.urlsafe_b64encode(bytes(decoded, 'utf-8'))


def update_servers():
    global servers
    servers = ss_free.main()
    global encoded
    decoded = list()
    for i in servers:
        for j in i['data']:
            if j['uri'][2] is 'r':
                decoded.append(j['uri'])
    decoded = '\n'.join(decoded)
    encoded = base64.urlsafe_b64encode(bytes(decoded, 'utf-8'))


counter_path = os.path.expanduser('~/python/counter')


def counter(counter_path=counter_path):
    if not os.path.exists(os.path.split(counter_path)[0]):
        os.makedirs(os.path.split(counter_path)[0])
    if not os.path.exists(counter_path):
        open(counter_path, 'w').write('0')
    count = int(open(counter_path).readline())
    open(counter_path, 'w').write(str(count + 1))
    if count % 15 == 0:
        update_thread = threading.Thread(target=update_servers)
        update_thread.start()
    return count


def gen_canvas_nest():
    """为背景很绚丽的特效生成随机参数
    """
    color = ','.join([str(random.randint(0, 255)) for i in range(3)])
    opacity = str(random.random() + 0.5)
    count = str(random.randint(0, 150))
    return color, opacity, count


@app.route('/')
def index():
    color, opacity, count = gen_canvas_nest()
    return render_template(
        'index.html',
        servers=servers,
        ss=ss[random.randint(0, len(ss) - 1)],
        counter=counter(),
        color=color,
        opacity=opacity,
        count=count,
        ctime=curtime,
    )


@app.route('/<string:path>')
def pages(path):
    print(path)
    try:
        a, b = path.split('-')
        a, b = int(a), int(b)
    except Exception:
        abort(404)

    uri = servers[a]['data'][b]['decoded_url'] if 'decoded_url' in servers[a]['data'][b] else ''
    remarks = servers[a]['data'][b]['remarks'] if 'remarks' in servers[a]['data'][b] else 'None'
    server = servers[a]['data'][b]['server'] if 'server' in servers[a]['data'][b] else 'None'
    server_port = servers[a]['data'][b]['server_port'] if 'server_port' in servers[a]['data'][b] else 'None'
    password = servers[a]['data'][b]['password'] if 'password' in servers[a]['data'][b] else 'None'
    method = servers[a]['data'][b]['method'] if 'method' in servers[a]['data'][b] else 'None'
    ssr_protocol = servers[a]['data'][b]['ssr_protocol'] if 'ssr_protocol' in servers[a]['data'][b] else 'None'
    obfs = servers[a]['data'][b]['obfs'] if 'obfs' in servers[a]['data'][b] else 'None'
    href = servers[a]['data'][b]['href'] if 'href' in servers[a]['data'][b] else 'None'
    json = servers[a]['data'][b]['json'] if 'json' in servers[a]['data'][b] else 'None'
    obfsparam = servers[a]['data'][b]['obfsparam'] if 'obfsparam' in servers[a]['data'][b] else 'None'
    protoparam = servers[a]['data'][b]['protoparam'] if 'protoparam' in servers[a]['data'][b] else 'None'
    color, opacity, count = gen_canvas_nest()

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
        color=color,
        opacity=opacity,
        count=count,
        json=json,
        obfsparam=obfsparam,
        protoparam=protoparam,
    )


@app.route('/subscribe')
def subscribe():
    return encoded


@app.route('/json')
def subscribe_json():
    return random.sample(random.sample(servers, 1)[0]['data'], 1)[0]['json']


@app.route('/js/<path:path>')
def send_jsadfsadfs(path):
    return send_from_directory('js', path)


@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static', 'favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    color, opacity, count = gen_canvas_nest()
    return render_template(
        '404.html',
        color=color,
        opacity=opacity,
        count=count,
    ), 404


print('部署完成')
