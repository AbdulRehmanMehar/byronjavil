# -*- coding: utf-8 -*-
# app/api/state.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server
from app.models import OrderState

from .utils import token_required

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("supervisor")


@ns.route('/states')
class SupervisorStateCollection(Resource):

    @api.doc(security='apikey')
    @token_required
    def get(self):

        result = list()

        states = OrderState.select()

        for state in states:
            result.append(state.state)

        return result
