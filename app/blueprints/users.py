# -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request, flash, redirect, url_for, session
from flask.ext.login import login_user, logout_user, login_required, current_user

from app.forms import LoginForm, RegisterForm, EditForm, ForgotForm
from app.extensions import db
from app.models import Bruker
from app.messages import *
from app.utils import flash_errors

blueprint = Blueprint('users', __name__)


@blueprint.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        bruker = Bruker.query.filter_by(email=form.email.data, passord=form.passord.data).first()

        if bruker is None:
            flash(USR_WRONG_USRPWD, FLASH_ERROR)
            return redirect(url_for('users.login'))

        if bruker.status == USR_NOTACTIVE:
            flash(USR_DEACTIVEATED, FLASH_INFO)
            return redirect(url_for('users.login'))

        login_user(bruker)
        flash(USR_LOGGEDIN, FLASH_SUCCESS)
        return redirect(request.args.get("next") or url_for('pages.index'))
    else:
        if form.errors:
            flash_errors(form)

        return render_template('forms/login.html', form=form)


@blueprint.route('/user/logout')
@login_required
def logout():
    if session.get('ski'):
        session['ski'] = []

    if session.get('liftpass'):
        session['liftpass'] = []

    flash(USR_LOGGEDOUT, FLASH_INFO)
    logout_user()
    return redirect(url_for('pages.index'))


@blueprint.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        user = Bruker(email=form.email.data,
                      passord=form.passord.data,
                      fornavn=form.fornavn.data,
                      etternavn=form.etternavn.data,
                      status=USR_ACTIVE,
                      telefon=form.telefon.data)

        db.session.add(user)
        db.session.commit()

        flash(USR_REGISTRED, FLASH_SUCCESS)
        return redirect(url_for('users.login'))
    else:
        if form.errors:
            flash_errors(form)

        return render_template('forms/register.html', form=form)


@blueprint.route('/user/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(request.form)

    if form.validate_on_submit():
        bruker = Bruker.query.filter_by(id=current_user.get_id()).first()
        bruker.passord = form.passord.data
        bruker.telefon = form.telefon.data

        db.session.commit()

        flash(USR_ACCUPDT, FLASH_SUCCESS)
        return redirect(url_for('pages.index'))
    else:
        if form.errors:
            flash_errors(form)

        # pre-fill data i alle tekstfeldt
        form.email.data = current_user.email
        form.passord.data = current_user.passord
        form.passord_igjen.data = current_user.passord
        form.fornavn.data = current_user.fornavn
        form.etternavn.data = current_user.etternavn
        form.telefon.data = current_user.telefon

        return render_template('forms/edit.html', form=form, current_user=current_user)


@blueprint.route('/user/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        bruker = Bruker.query.filter_by(id=current_user.get_id()).first()
        bruker.status = USR_NOTACTIVE

        db.session.commit()
        logout_user()
        flash(USR_DEACTIVEATED, FLASH_INFO)
        return redirect(url_for('pages.index'))

    return redirect(url_for('users.edit'))
