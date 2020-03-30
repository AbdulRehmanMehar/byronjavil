# -*- coding: utf-8 -*-
# app/api/order.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server

from .utils import token_required, role_required

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("supervisor")


@ns.route('/customers')
class SupervisorOrderCollection(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def get(self):

        result = list()

        dbo = app.customer_dbo

        customers = dbo.read_all()

        for customer in customers:
            result.append(model_to_dict(customer))

        return result

    # @ns.expect(customer_model)
    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def post(self):

        payload = api.payload

        dbo = app.customer_dbo

        customer = dbo.create(**payload)

        return model_to_dict(customer)


@ns.route('/customers/<int:_id>')
class SupervisorOrder(Resource):
    
    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def get(self, _id):

        dbo = app.customer_dbo

        customer = dbo.read(_id)

        return model_to_dict(customer)

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def put(self, _id):

        payload = api.payload

        dbo = app.customer_dbo

        dbo.update(_id, **payload)

        return True

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def delete(self, _id):

        dbo = app.customer_dbo

        dbo.delete(_id)

        return True