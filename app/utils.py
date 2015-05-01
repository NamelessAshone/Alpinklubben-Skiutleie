# -*- coding: utf-8 -*-

from flask import flash
from app.messages import *


# flasher alle feil vi får i wtforms bla.
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, FLASH_ERROR)


def fiks_encoding(streng):
    return streng.decode('UTF-8')