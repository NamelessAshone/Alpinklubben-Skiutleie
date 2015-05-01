# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
