# -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import current_user, login_user

from app.forms import LoginForm
from app.messages import *
from app.models import Bruker
from app.utils import flash_errors

blueprint = Blueprint('pages', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        bruker = Bruker.query.filter_by(email=form.email.data, passord=form.passord.data).first()

        if bruker is None:
            flash(USR_WRONG_USRPWD, FLASH_ERROR)
            return redirect(url_for('pages.index'))

        if bruker.status == USR_NOTACTIVE:
            flash(USR_DEACTIVEATED, FLASH_INFO)
            return redirect(url_for('pages.index'))

        login_user(bruker)
        flash(USR_LOGGEDIN, FLASH_SUCCESS)
        return redirect(request.args.get("next") or url_for('pages.index'))
    else:
        if form.errors:
            flash_errors(form)

    return render_template('pages/index.html', current_user=current_user, form=form)


@blueprint.route('/about')
def about():
    return render_template('pages/about.html', form=LoginForm(request.form))

