#!/usr/bin/env python
# -*- utf-8 -*-

import os
from flask_script import Manager, Server
from app import app

port = os.environ.get('PORT')

manager = Manager(app)

manager.add_command(
    "runserver", Server(host="0.0.0.0", port=port, use_debugger=True)
)

if __name__ == '__main__':
    manager.run()
