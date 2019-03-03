#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask_script import Manager, Server
from ssshare.main import app

port = os.environ.get('PORT')

manager = Manager(app)

manager.add_command(
    "runserver", Server(host="0.0.0.0", port=port, use_debugger=False)
)
manager.add_command(
    "debug", Server(host="0.0.0.0", port=8080, use_debugger=True)
)

if __name__ == '__main__':
    manager.run()
