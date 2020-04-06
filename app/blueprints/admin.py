# -*- coding: utf-8 -*-
# app/blueprints/admin.py

from flask import render_template, current_app
from flask_login import login_required, current_user

from . import admin
from .utils import role_required, get_credentials


@admin.route('/admin')
@login_required
@role_required(["ADMIN"])
def admin_page():

    credentials = get_credentials()
    
    return render_template("admin.html", credentials=credentials)
