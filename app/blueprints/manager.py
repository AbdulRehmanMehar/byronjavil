# -*- coding: utf-8 -*-
# app/blueprints/manager.py

from flask import render_template, current_app
from flask_login import login_required, current_user

from . import manager
from .utils import role_required, get_credentials

@manager.route('/manager')
@login_required
@role_required(["SUPERVISOR/MANAGER", "MANAGER"])
def manager_page():

    credentials = get_credentials()
    
    return render_template("manager.html", credentials=credentials)

@manager.route('/manager/orders/<int:order_id>')
@login_required
@role_required(["SUPERVISOR/MANAGER", "MANAGER"])
def manager_order_page(order_id):

    credentials = get_credentials()
    
    return render_template("manager_order.html", order_id=order_id, credentials=credentials)