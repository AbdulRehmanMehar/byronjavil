# -*- coding: utf-8 -*-
# app/api/order_type.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server

from .utils import token_required, role_required

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("supervisor")

order_type_model = api.model("order_type_model", {
    'type': fields.String(required=True, description='Order type')
})


@ns.route('/order-type')
class SupervisorOrderTypeCollection(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def get(self):

        result = list()

        dbo = app.order_type_dbo

        order_types = dbo.read_all()

        for order_type in order_types:
            result.append(model_to_dict(order_type))

        return result

    @ns.expect(order_type_model)
    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def post(self):

        payload = api.payload

        _type = payload["type"]

        dbo = app.order_type_dbo

        order_type = dbo.create(_type)

        return model_to_dict(order_type)


@ns.route('/order-type/<int:_id>')
class SupervisorOrderType(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def get(self, _id):

        dbo = app.order_type_dbo

        order_type = dbo.read(_id)

        return model_to_dict(order_type)
    
    @ns.expect(order_type_model)
    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def put(self, _id):

        payload = api.payload

        _type = payload["type"]

        dbo = app.order_type_dbo

        dbo.update(_id, _type)

        return True

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def delete(self, _id):

        dbo = app.order_type_dbo

        dbo.delete(_id)

        return True
