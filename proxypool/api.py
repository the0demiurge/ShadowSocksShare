from flask import Flask, g
from proxypool.db import RedisClient
import random
import logging
import time
from proxypool.ascii import ss_title
from flask import send_from_directory, render_template, abort

__all__ = ['app']

app = Flask(__name__)

curtime = time.ctime()

servers = list()

def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


def get_servers():
    try:
        global servers
        servers = []
        con = get_conn()
        results = con.all()
        for result in results:
            servers.append(eval(result))
    except Exception as e:
        return None
        logging.exception(e, stack_info=True)


def gen_canvas_nest():
    """为背景很绚丽的特效生成随机参数
    """
    color = ','.join([str(random.randint(0, 255)) for i in range(3)])
    opacity = str(random.random() + 0.5)
    count = str(random.randint(0, 150))
    return color, opacity, count


@app.route('/')
def index():
    try:
        color, opacity, count = gen_canvas_nest()
        return render_template(
            'index.html',
            ss=ss_title[random.randint(0, len(ss_title) - 1)],
            color=color,
            opacity=opacity,
            count=count,
            ctime=curtime,
        )
    except Exception as e:
        logging.exception(e, stack_info=True)



@app.route('/<string:path>')
def pages(path):
    print(path)
    global servers
    try:
        a, b = path.split('-')
        a = int(a)
    except Exception:
        abort(404)

    if a >= len(servers):
        abort(404)

    try:
        uri = servers[a].get('decoded_url', '')
        remarks = servers[a].get('remarks', 'None')
        server = servers[a].get('server', 'None')
        server_port = servers[a].get('server_port', 'None')
        password = servers[a].get('password', 'None')
        method = servers[a].get('method', 'None')
        ssr_protocol = servers[a].get('ssr_protocol', 'None')
        obfs = servers[a].get('obfs', 'None')
        href = servers[a].get('href', 'None')
        json = servers[a].get('json', 'None')
        obfsparam = servers[a].get('obfsparam', 'None')
        protoparam = servers[a].get('protoparam', 'None')

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
            server_data=servers[a],
            color=color,
            opacity=opacity,
            count=count,
            json=json,
            obfsparam=obfsparam,
            protoparam=protoparam,
        )
    except Exception as e:
        logging.exception(e, stack_info=True)


@app.route('/json')
def subscribe_json():
    conn = get_conn()
    return eval(conn.random()).get['json']


@app.route('/random')
def get_proxy():
    """
    Get a proxy
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()


@app.route('/detail')
def get_all_proxy():
    try:
        global servers
        get_servers()
        color, opacity, count = gen_canvas_nest()
        return render_template(
            'detail.html',
            servers=servers,
            color=color,
            opacity=opacity,
            count=count,
        )
    except Exception as e:
        logging.exception(e, stack_info=True)


@app.route('/count')
def get_counts():
    """
    Get the count of proxies
    :return: 代理池总量
    """
    conn = get_conn()
    return str(conn.count())


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/html/<path:path>')
def static_html(path):
    try:
        color, opacity, count = gen_canvas_nest()
        return render_template(
            path,
            color=color,
            opacity=opacity,
            count=count,)
    except Exception as e:
        logging.exception(e)
        abort(404)


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


if __name__ == '__main__':
    app.run()