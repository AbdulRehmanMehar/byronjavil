# -*- coding: utf-8 -*-
# app/blueprints/supervisor.py

from flask import render_template, current_app
from flask_login import login_required, current_user

from . import supervisor
from .utils import role_required, get_credentials

@supervisor.route('/supervisor')
@login_required
@role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
def supervisor_page():

    credentials = get_credentials()
    
    return render_template("supervisor.html", credentials=credentials)