# -*- coding: utf-8 -*-
# app/api/research.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server
from app.models import OrderState, OrderType
from app.email import send_mail_template

from .utils import token_required, role_required, get_current_user

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("research")


@ns.route('/orders')
class ResearchOrderCollectionResource(Resource):
    
    @api.doc(security='apikey')
    @token_required
    @role_required(["RESEARCH"])
    def get(self):

        dbo = app.order_dbo
        user = get_current_user()

        response = list()

        orders = dbo.read_all()

        for order in orders:
            if dbo.verify_authority(order.id, user):
                
                result = model_to_dict(order)

                result["assigned_date"] = str(result["assigned_date"])
                result["due_date"] = str(result["due_date"])
                
                response.append(result)

        return response


@ns.route('/orders/<int:_id>')
class ResearchOrderResource(Resource):
    
    @api.doc(security='apikey')
    @token_required
    @role_required(["RESEARCH"])
    def get(self, _id):

        dbo = app.order_dbo
        user = get_current_user()

        if not dbo.verify_authority(_id, user):
            return 401, "Not authorized in this order"
        
        order = dbo.read(_id)

        response = model_to_dict(order)

        response["assigned_date"] = str(response["assigned_date"])
        response["due_date"] = str(response["due_date"])

        return response


@ns.route('/orders/<int:_id>/mark-completed')
class ResearchCompleteActionResource(Resource):
    
    @api.doc(security='apikey')
    @token_required
    @role_required(["RESEARCH"])
    def post(self, _id):

        dbo = app.order_dbo
        user = get_current_user()

        if not dbo.verify_authority(_id, user):
            return 401, "Not authorized in this order"

        dbo.set_state(_id, "DATA_ENTRY")
        
        order = dbo.read(_id)
        order.research_completed = True
        order.save()

        data_user = order.data_user

        send_mail_template("ASSIGN_DATA", order, username=data_user.username, from_email="admin@pams.com", to_emails=[data_user.email])

        return True