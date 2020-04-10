# -*- coding: utf-8 -*-
# app/blueprints/company.py

from flask import render_template, current_app
from flask_login import login_required, current_user

from . import company
from .utils import role_required, get_credentials


@company.route('/supervisor/companies/<int:company_id>')
@login_required
@role_required(["SUPERVISOR", "SUPERVISOR/MANAGER", "DATA"])
def supervisor_company_page(company_id):

    credentials = get_credentials()
    
    return render_template("company_detail.html", company_id=company_id, credentials=credentials)


@company.route('/data/companies/<int:company_id>')
@login_required
@role_required(["DATA"])
def data_company_page(company_id):

    credentials = get_credentials()
    
    return render_template("company_detail.html", company_id=company_id, credentials=credentials)
