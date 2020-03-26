# -*- coding: utf-8 -*-
# app/blueprints/supervisor.py

from flask import render_template, current_app
from flask_login import login_required, current_user

from . import supervisor
from .utils import role_required

@supervisor.route('/supervisor')
@login_required
@role_required(["SUPERVISOR"])
def supervisor_page():

    dbo = current_app.user_dbo

    user = dbo.read_by_id(current_user.id)
    
    render_template("supervisor.html")