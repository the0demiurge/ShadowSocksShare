#!/usr/bin/env python
# -*- utf-8 -*-
import test
from app import app as application
import logging
import os

if 'PORT' in os.environ:
    port = int(os.environ['PORT'])
else:
    port = 8080


if __name__ == '__main__':
    try:
        # application.run(host='0.0.0.0', port=port)
        from wsgiref.simple_server import make_server
        httpd = make_server('0.0.0.0', port, application)
        httpd.serve_forever()
    except Exception as e:
        logging.exception(e, stack_info=True)
