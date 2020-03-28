# -*- coding: utf-8 -*-
# app/blueprints/data.py

from flask import render_template, current_app
from flask_login import login_required, current_user

from . import data
from .utils import role_required, get_credentials

@data.route('/data')
@login_required
@role_required(["DATA"])
def data_page():

    credentials = get_credentials()
    
    return render_template("data.html", credentials=credentials)