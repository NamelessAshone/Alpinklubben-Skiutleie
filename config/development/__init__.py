# -*- coding: utf-8 -*-

import os

DEBUG = True
SECRET_KEY = 'sexy utleie'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
HOST = 'localhost'
PORT = int(os.environ.get('PORT', 5000))
