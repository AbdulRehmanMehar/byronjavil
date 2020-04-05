# -*- coding: utf-8 -*-
# app/blueprints/home.py

from flask import render_template

from . import home

@home.route('/')
def home_page():
    
    return render_template("home.html")