# -*- coding: utf-8 -*-
# app/api/order.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server
from app.models import OrderState, OrderType
from app.email import send_mail_template

from .utils import token_required, role_required

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("supervisor")

order_model = api.model("users_model", {
    'address': fields.String(required=True, description='Property address'),
    'username': fields.String(required=True, description='Assigned Username'),
    'customer_id': fields.Integer(required=True, description='Assigned company'),
    'type': fields.String(required=True, description='Order type'),
    'state': fields.String(required=True, description='Order state')
})


@ns.route('/orders')
class SupervisorOrderCollection(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def get(self):

        result = list()
        
        dbo = app.order_dbo
        orders = dbo.read_all()

        for order in orders:
            response = model_to_dict(order)

            response["date_assigned"] = str(response["date_assigned"])
            response["due_date"] = str(response["due_date"])
            
            result.append(response)

        return result

    @ns.expect(order_model)
    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def post(self):

        payload = api.payload

        dbo = app.order_dbo
        user_dbo = app.user_dbo
        customer_dbo = app.customer_dbo

        research_id = payload["research_id"]
        data_id = payload["data_id"]
        customer_id = payload["customer_id"]

        research_user = user_dbo.read_by_id(research_id)
        data_user = user_dbo.read_by_id(data_id)
        customer = customer_dbo.read(customer_id)

        data = {
            "address": payload["address"],
            "research_user": research_user,
            "data_user": data_user,
            "customer": customer
        }

        order = dbo.create(**data)

        state = "RESEARCH"
        order_state = OrderState.select().where(OrderState.state==state).get()
        order_type = OrderType.select().where(OrderType.order_type==payload["type"]).get()

        order.kind = order_type
        order.state = order_state

        order.save()

        response = model_to_dict(order)

        response["date_assigned"] = str(response["date_assigned"])
        response["due_date"] = str(response["due_date"])

        send_mail_template("ASSIGN_RESEARCH", order, username=research_user.username, from_email="admin@pams.com", to_emails=[research_user.email])

        return response


@ns.route('/orders/<int:_id>')
class SupervisorOrder(Resource):
    
    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def get(self, _id):

        dbo = app.order_dbo

        order = dbo.read(_id)

        response = model_to_dict(order)

        response["date_assigned"] = str(response["date_assigned"])
        response["due_date"] = str(response["due_date"])

        return response

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def delete(self, _id):

        dbo = app.order_dbo

        dbo.delete(_id)

        return True