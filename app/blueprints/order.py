# -*- coding: utf-8 -*-

from flask import render_template, Blueprint, redirect, url_for, session, request, flash, g
from flask.ext.login import login_required, current_user

from app.models import Ski, Heiskort, Ordre, Ordre_Heiskort, Ordre_Ski, Handleliste, db
from app.messages import *

blueprint = Blueprint('order', __name__)


@blueprint.before_request
def sjekkLister():
    # sørg for at våres handlelister er satt opp
    if not session.get('ski'):
        session['ski'] = []
    if not session.get('liftpass'):
        session['liftpass'] = []


@blueprint.route('/order/order')
@login_required
def order():
    return render_template('order/order.html',
                           ski=Ski.query.all(),
                           liftpass=Heiskort.query.all())


@blueprint.route('/order/basket/', methods=['GET', 'POST'])
@login_required
def basket():
    if request.method == 'POST':
        pris = float(request.form["periode"])
        id = int(request.args.get("id"))
        type = str(request.args.get("type"))

        try:
            session[type] += [[id, pris]]
        except KeyError:
            session[type] = [[id, pris]]

        flash(ORD_ADDED, FLASH_INFO)

    total_pris, skis, lift = settOppOrdre()

    return render_template('order/basket.html',
                           skis=skis,
                           lift=lift,
                           total_pris=total_pris)


@blueprint.route('/order/remove/<type>/<index>')
@login_required
def remove(type, index):
    del session[type][int(index)]
    flash(ORD_REMOVED, FLASH_INFO)
    return redirect(url_for('order.basket'))


@blueprint.route('/order/receipt')
@login_required
def receipt():
    total_pris, skis, lift = settOppOrdre()

    order = Ordre(current_user.get_id(), total_pris)

    db.session.add(order)       # her må vi først legge til
    db.session.flush()          # for å siden initiere den i databasen
    db.session.refresh(order)   # for å siden kunne hent ut ordre id
    # dette grunnet at sqlite/sqlalchemy ikke støtter transaction eller lignende.

    order_id = order.get_id()

    for s in skis:
        db.session.add(Ordre_Ski(order_id, s.id))

    for l in lift:
        db.session.add(Ordre_Heiskort(order_id, l.id))

    db.session.commit()

    session['ski'] = None
    session['liftpass'] = None

    flash(ORD_THANKS, FLASH_SUCCESS)

    return render_template('order/receipt.html',
                           total_pris=total_pris,
                           skis=skis,
                           lift=lift,
                           order=order)


def settOppOrdre():
    skis = []
    lift = []
    total_pris = 0

    for s in session.get('ski'):
        ski = Ski.query.filter_by(id=s[0]).first()

        total_pris += s[1]
        skis.append(Handleliste(ski.id, ski.navn, ski.beskrivelse, s[1]))

    for s in session.get('liftpass'):
        liftpass = Heiskort.query.filter_by(id=s[0]).first()

        total_pris += liftpass.pris
        lift.append(liftpass)

    return total_pris, skis, lift


@blueprint.after_request
def per_request_callbacks(response):
    for func in getattr(g, 'call_after_request', ()):
        response = func(response)
    return response