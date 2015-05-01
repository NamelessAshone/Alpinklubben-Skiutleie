# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'pages.index'
