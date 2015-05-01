# -*- coding: utf-8 -*-
import logging
from flask import Flask

from app.models import *

from app.extensions import db, login_manager
extensions = (db, login_manager)

from app.blueprints import order, pages, user, stats
blueprints = (order, pages, user, stats)


# lag selve flask instansen
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    app.logger.setLevel(logging.DEBUG)

    # last inn moduler å blueprints
    configure_ext(app, extensions)
    configure_blueprints(app, blueprints)

    return app


# initiere alle flask moduler
def configure_ext(app, ext):
    for e in ext:
        e.init_app(app)


# initere alle blueprints
def configure_blueprints(app, bprints):
    for b in bprints:
        app.register_blueprint(b.blueprint)