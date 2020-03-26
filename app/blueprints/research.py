# -*- coding: utf-8 -*-
# app/blueprints/research.py

from flask import render_template, current_app
from flask_login import login_required, current_user

from . import research
from .utils import role_required

@research.route('/research')
@login_required
@role_required(["RESEARCH"])
def research_page():

    dbo = current_app.user_dbo

    user = dbo.read_by_id(current_user.id)
    
    render_template("research.html")