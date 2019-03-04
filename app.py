#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ssshare.main import app as application
import logging
import os
print(__name__)
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
