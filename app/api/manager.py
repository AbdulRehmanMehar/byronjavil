# -*- coding: utf-8 -*-
# app/api/manager.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server
from app.models import OrderState, OrderType

from .utils import token_required, role_required, get_current_user

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("manager")


@ns.route('/orders')
class ManagerOrderCollectionResource(Resource):
    
    @api.doc(security='apikey')
    @token_required
    @role_required(["MANAGER", "SUPERVISOR/MANAGER"])
    def get(self):

        dbo = app.order_dbo
        user = get_current_user()

        response = dict()

        orders = dbo.read_all()

        order_list = list()

        for order in orders:

            order_id = order.id
            address = order.address
            due_date = str(order.due_date)
            company = order.customer.company
            research = order.research_user.username
            data = order.data_user.username
            state = order.state.state

            url = '<a href="/manager/orders/{}">View</a>'.format(order_id)

            result = [order_id, address, due_date, company, research, data, state, url]
            # result = model_to_dict(order)

            # result["date_assigned"] = str(result["date_assigned"])
            # result["due_date"] = str(result["due_date"])

            # response.append(result)

            order_list.append(result)

        response["data"] = order_list

        return response


@ns.route('/orders/<int:_id>')
class ManagerOrderResource(Resource):
    
    @api.doc(security='apikey')
    @token_required
    @role_required(["MANAGER", "SUPERVISOR/MANAGER"])
    def get(self, _id):

        dbo = app.order_dbo
        user = get_current_user()

        if not dbo.verify_authority(_id, user):
            return 401, "Not authorized in this order"
        
        order = dbo.read(_id)

        response = model_to_dict(order)

        response["date_assigned"] = str(response["date_assigned"])
        response["due_date"] = str(response["due_date"])

        return response