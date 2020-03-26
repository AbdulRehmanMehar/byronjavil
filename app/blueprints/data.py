# -*- coding: utf-8 -*-
# app/blueprints/data.py

from flask import render_template, current_app
from flask_login import login_required, current_user

from . import data
from .utils import role_required

@data.route('/data')
@login_required
@role_required(["DATA"])
def data_page():

    dbo = current_app.user_dbo

    user = dbo.read_by_id(current_user.id)
    
    render_template("data.html")