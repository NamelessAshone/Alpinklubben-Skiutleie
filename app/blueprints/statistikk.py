# -*- coding: utf-8 -*-

from flask import render_template, Blueprint
from flask.ext.login import login_required

from app.extensions import db

import pygal
from pygal.style import LightStyle

blueprint = Blueprint('statistikk', __name__)

@blueprint.route('/statistikk/statistikk')
@blueprint.route('/statistikk/statistikk/<type>')
@login_required
def render(type=1):
    title, data = db_data(type)
    chart = pygal.Bar(style=LightStyle)
    chart.title = title

    for d in data:
        chart.add(d[0], [d[1]])

    chart = chart.render(is_unicode=True, width=640, height=400, explicit_size=True)
    return render_template('statistikk/graf.html', chart=chart)


def db_data(p):
    p = int(p)
    if p == 1:
        title = 'Hvilke er dem mest populere skiene?'
        data = db.engine.execute("SELECT Ski.navn, COUNT(Ski.id) "
                                 "FROM Ski "
                                 "JOIN Ordre_Ski ON Ordre_Ski.ski_id = Ski.id "
                                 "GROUP BY Ski.navn")
    elif p == 2:
        title = 'Antal dags, uke og sesonkort som er solgt.'
        data = db.engine.execute("SELECT Heiskort.navn, COUNT(Heiskort.id) "
                                 "FROM Heiskort "
                                 "JOIN Ordre_Heiskort ON Ordre_Heiskort.heis_id = Heiskort.id "
                                 "GROUP BY Heiskort.navn")
    return title, data