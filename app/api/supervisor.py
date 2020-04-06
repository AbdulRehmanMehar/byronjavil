# -*- coding: utf-8 -*-
# app/api/supervisor.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server

from .utils import token_required, role_required, get_current_user

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("supervisor")


@ns.route('/order-type')
class SupervisorOrderTypeCollectionResource(Resource):

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


@ns.route('/users')
class SupervisorUsersCollectionResource(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def get(self):

        result = list()

        dbo = app.user_dbo

        users = dbo.read_all()

        for user in users:

            user = model_to_dict(user)
            del user["password"]
            
            result.append(user)

        return result


@ns.route('/customers')
class SupervisorCustomerCollectionResource(Resource):

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