# -*- coding: utf-8 -*-

from app.extensions import login_manager
from app.models import *


# sørg for at bruker objektet er lastet inn til en hver tid
@login_manager.user_loader
def user_loader(userid):
    return Bruker.query.get(userid)