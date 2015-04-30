# -*- coding: utf-8 -*-

from flask import render_template, Blueprint
from flask_login import current_user

blueprint = Blueprint('pages', __name__)


@blueprint.route('/')
def index():
    return render_template('pages/index.html', current_user=current_user)


@blueprint.route('/about')
def about():
    return render_template('pages/about.html')

