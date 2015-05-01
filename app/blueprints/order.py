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

    sum, skis, lift = settOppOrdre()
    pris = Pris(sum)

    print pris

    return render_template('order/basket.html',
                           skis=skis,
                           lift=lift,
                           sum=pris.sum,
                           mva=pris.mva,
                           total=pris.total,
                           rabatt=pris.rabatt)


@blueprint.route('/order/remove/<type>/<index>')
@login_required
def remove(type, index):
    del session[type][int(index)]
    flash(ORD_REMOVED, FLASH_INFO)
    return redirect(url_for('order.basket'))


@blueprint.route('/order/receipt')
@login_required
def receipt():
    sum, skis, lift = settOppOrdre()
    pris = Pris(sum)

    order = Ordre(current_user.get_id(), pris.total)

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
                           skis=skis,
                           lift=lift,
                           order=order,
                           sum=pris.sum,
                           mva=pris.mva,
                           total=pris.total,
                           rabatt=pris.rabatt)


def settOppOrdre():
    skis = []
    lift = []
    sum = 0

    for s in session.get('ski'):
        ski = Ski.query.filter_by(id=s[0]).first()

        sum += s[1]
        skis.append(Handleliste(ski.id, ski.navn, ski.beskrivelse, s[1]))

    for s in session.get('liftpass'):
        liftpass = Heiskort.query.filter_by(id=s[0]).first()

        sum += liftpass.pris
        lift.append(liftpass)

    return sum, skis, lift


class Pris(object):
    sum = 0
    rabatt = 0
    mva = 0
    total = 0

    def __init__(self, sum):
        self.sum = sum
        self.rabatt = round(self.sum * 0.15 if len(session['ski']) >= 4 else 0, 2)
        self.mva = round(self.sum * 0.25, 2)
        self.total = round(self.sum + self.mva, 2)

    def __repr__(self):
        return '<Sum %s - Rabatt %s - MVA %s - Total %s>' % (self.sum, self.rabatt, self.mva, self.total)