# -*- coding: utf-8 -*-
# app/blueprints/manager.py

from flask import render_template, current_app
from flask_login import login_required, current_user

from . import manager
from .utils import role_required

@manager.route('/manager')
@login_required
@role_required(["SUPERVISOR/MANAGER", "MANAGER"])
def manager_page():

    dbo = current_app.user_dbo

    user = dbo.read_by_id(current_user.id)
    
    return render_template("manager.html")