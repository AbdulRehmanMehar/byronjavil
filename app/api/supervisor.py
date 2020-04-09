# -*- coding: utf-8 -*-
# app/api/supervisor.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server
from app.models import OrderState

from .utils import token_required, role_required, get_current_user

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("supervisor")


@ns.route('/states')
class SupervisorStateCollectionResource(Resource):

    @api.doc(security='apikey')
    @token_required
    def get(self):

        result = list()

        states = OrderState.select()

        for state in states:
            result.append(state.state)

        return result


@ns.route('/client-code')
class SupervisorClientCodeCollectionResource(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def get(self):

        result = list()

        dbo = app.client_code_dbo

        client_codes = dbo.read_all()

        for client_code in client_codes:
            result.append(model_to_dict(client_code))

        return result


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


@ns.route('/companies')
class SupervisorCompaniesCollectionResource(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def get(self):

        result = list()

        dbo = app.company_dbo

        companies = dbo.read_all()

        for company in companies:
            result.append(model_to_dict(company))

        return result


@ns.route('/orders/<int:_id>/mark-picture')
class SupervisorMarkPictureResource(Resource):
    
    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR"])
    def post(self, _id):

        dbo = app.order_dbo
        user = get_current_user()

        if not dbo.verify_authority(_id, user):
            return 401, "Not authorized in this order"

        dbo.mark_supervisor_picture(_id)
        
        return True