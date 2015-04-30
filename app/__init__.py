# -*- coding: utf-8 -*-
import logging
from os import path
from flask import Flask

from app.models import *
from app.blueprints import pages, order, users, statistikk
from app.extensions import login_manager, db

extensions = (db, login_manager)
blueprints = (order, pages, users, statistikk)


# lag selve flask instansen
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    app.logger.setLevel(logging.DEBUG)

    # last inn moduler å blueprints
    configure_ext(app, extensions)
    configure_blueprints(app, blueprints)

    # en "hacky" måte å sett opp database med tilhørende "dummy data"
    with app.app_context():
        if not path.isfile(path.join(app.config['BASE_DIR'], 'database.db')):
            from app.models import sett_data
            db.create_all()
            sett_data()

    return app


# initiere alle flask moduler
def configure_ext(app, ext):
    for e in ext:
        e.init_app(app)


# initere alle blueprints
def configure_blueprints(app, bprints):
    for b in bprints:
        app.register_blueprint(b.blueprint)
