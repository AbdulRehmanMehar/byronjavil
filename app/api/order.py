# -*- coding: utf-8 -*-
# app/api/order.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server
from app.models import OrderState, OrderType
from app.email import send_mail_template

from .utils import token_required, role_required, order_states

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("supervisor")

order_model = api.model("users_model", {
    'address': fields.String(required=True, description='Property address'),
    'username': fields.String(required=True, description='Assigned Username'),
    'company_id': fields.Integer(required=True, description='Assigned company'),
    'client_code': fields.String(required=True, description='Company client code'),
    'type': fields.String(required=True, description='Order type'),
    'state': fields.String(required=True, description='Order state'),
    'assigned_date': fields.String(required=True, description='Due date'),
    'due_date': fields.String(required=True, description='Due date')
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

            response["assigned_date"] = str(response["assigned_date"])
            response["due_date"] = str(response["due_date"])
            response["state"]["state"] = order_states[response["state"]["state"]]
            
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
        type_dbo = app.order_type_dbo
        company_dbo = app.company_dbo
        client_dbo = app.client_code_dbo

        print(payload)

        research_id = payload["research_id"]
        data_id = payload["data_id"]
        company_id = payload["company_id"]

        data_user = user_dbo.read_by_id(data_id)
        company = company_dbo.read(company_id)
        order_type = type_dbo.read_by_type(payload["type"])
        client_code = client_dbo.read_by_code(payload["client_code"])
        
        

        if research_id:
            research_user = user_dbo.read_by_id(research_id)
            state = "RESEARCH"

        else:
            
            state = "DATA_ENTRY"
            research_user = None

        order_state = OrderState.select().where(OrderState.state==state).get()
        
        data = {
            "address": payload["address"],
            "data_user": data_user,
            "research_user": research_user,
            "company": company,
            "due_date": payload["due_date"],
            "assigned_date": payload["assigned_date"],
            "client_code": client_code,
            "kind": order_type,
            "state": order_state
        }
        
        order = dbo.create(**data)

        order.save()

        response = model_to_dict(order)

        response["assigned_date"] = str(response["assigned_date"])
        response["due_date"] = str(response["due_date"])
        response["state"]["state"] = order_states[response["state"]["state"]]

        if research_id:
            send_mail_template("ASSIGN_RESEARCH", order, username=research_user.username, from_email="admin@pams.com", to_emails=[research_user.email])
        else:
            send_mail_template("ASSIGN_DATA", order, username=data_user.username, from_email="admin@pams.com", to_emails=[data_user.email])

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

        response["assigned_date"] = str(response["assigned_date"])
        response["due_date"] = str(response["due_date"])
        response["state"]["state"] = order_states[response["state"]["state"]]

        return response

    @ns.expect(order_model)
    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def put(self, _id):

        payload = api.payload

        dbo = app.order_dbo
        user_dbo = app.user_dbo
        type_dbo = app.order_type_dbo
        company_dbo = app.company_dbo
        client_dbo = app.client_code_dbo

        research_id = payload["research_id"]
        data_id = payload["data_id"]
        company_id = payload["company_id"]

        research_user = user_dbo.read_by_id(research_id)
        data_user = user_dbo.read_by_id(data_id)
        company = company_dbo.read(company_id)
        order_type = type_dbo.read_by_type(payload["type"])
        client_code = client_dbo.read_by_code(payload["client_code"])
        state = "RESEARCH"
        order_state = OrderState.select().where(OrderState.state==state).get()

        data = {
            "address": payload["address"],
            "research_user": research_user,
            "data_user": data_user,
            "company": company,
            "due_date": payload["due_date"],
            "assigned_date": payload["assigned_date"],
            "client_code": client_code,
            "kind": order_type,
            "state": order_state
        }

        dbo.update(_id, **data)

        order = dbo.read(_id)
        send_mail_template("ASSIGN_RESEARCH", order, username=research_user.username, from_email="admin@pams.com", to_emails=[research_user.email])

        return True

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def delete(self, _id):

        dbo = app.order_dbo

        dbo.delete(_id)

        return True