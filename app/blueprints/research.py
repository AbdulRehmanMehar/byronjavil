# -*- coding: utf-8 -*-
# app/blueprints/research.py

from flask import render_template, current_app
from flask_login import login_required, current_user

from . import research
from .utils import role_required, get_credentials

@research.route('/research')
@login_required
@role_required(["RESEARCH"])
def research_page():

    credentials = get_credentials()
    
    return render_template("research.html", credentials=credentials)