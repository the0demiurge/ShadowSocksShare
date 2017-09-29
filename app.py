#!/usr/bin/env python
# -*- utf-8 -*-
from app import app as application
import logging


if __name__ == '__main__':
    try:
        application.run(host='0.0.0.0', port=8080)
    except Exception as e:
        logging.exception(e, stack_info=True)
    # from wsgiref.simple_server import make_server
    # httpd = make_server('localhost', 8051, application)
    # httpd.serve_forever()
