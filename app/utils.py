# -*- coding: utf-8 -*-

from flask import flash
from app.messages import *


# flasher alle feil vi får i wtforms bla.
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error), FLASH_ERROR)