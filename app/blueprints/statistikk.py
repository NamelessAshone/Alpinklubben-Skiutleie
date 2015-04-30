# -*- coding: utf-8 -*-

import pygal
from pygal.style import LightStyle
from datetime import datetime

from flask import render_template, Blueprint
from flask.ext.login import login_required

from app.extensions import db

blueprint = Blueprint('statistikk', __name__)


@blueprint.route('/statistikk/graf/')
@login_required
def graf():
    grafer = ('ski', 'cards', 'inntekt')

    return render_template('statistikk/graf.html', grafer=grafer)


@blueprint.route('/statistikk/svg/<type>.svg')
@login_required
def render(type):
    LightStyle.background = 'transparent'

    if type == 'ski':
        chart = pygal.Bar(style=LightStyle)
        chart.title = 'Hvilke er dem mest populere skiene?'
        data = db.engine.execute("SELECT Ski.navn, COUNT(Ski.id) "
                                 "FROM Ski "
                                 "JOIN Ordre_Ski ON Ordre_Ski.ski_id = Ski.id "
                                 "GROUP BY Ski.navn")
    elif type == 'cards':
        chart = pygal.Pie(style=LightStyle)
        chart.title = 'Hvilken er den meste populere kort typen?'
        data = db.engine.execute("SELECT Heiskort.navn, COUNT(Heiskort.id) "
                                 "FROM Heiskort "
                                 "JOIN Ordre_Heiskort ON Ordre_Heiskort.heis_id = Heiskort.id "
                                 "GROUP BY Heiskort.navn")
    elif type == 'inntekt':
        # denne funksjonen ville jo sett annerledes ut hvis at vi hadd mer data å gå på
        # men i med at vi kun har ett par dager med data så bruker vi kun det.
        chart = pygal.Bar(style=LightStyle)
        chart.title = 'Inntekt per dag.'
        data = db.engine.execute("SELECT strftime('%Y-%m-%d', Ordre.dato), SUM(Ordre.sum) AS totalt "
                                 "FROM Ordre "
                                 "GROUP BY strftime('%Y-%m-%d', Ordre.dato)")

    for d in data:
        chart.add(d[0], [d[1]])

    return chart.render_response()