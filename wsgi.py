#!/usr/bin/env python
# -*- utf-8 -*-
from app import app as application


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8051)
    # from wsgiref.simple_server import make_server
    # httpd = make_server('localhost', 8051, application)
    # httpd.serve_forever()
    print('初始化成功')
