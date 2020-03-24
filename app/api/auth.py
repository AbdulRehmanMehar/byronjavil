# -*- coding: utf-8 -*-
# app/api/auth.py

from flask_restplus import Resource
from playhouse.shortcuts import model_to_dict

from app.server import server

api = server.get_api()
ns = server.get_namespace("auth")