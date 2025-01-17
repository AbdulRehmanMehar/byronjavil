# -*- coding: utf-8 -*-
# app/api/data.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server
from app.models import OrderState, OrderType, OrderPicture
from app.email import send_mail_template

from .utils import token_required, role_required, get_current_user, order_states

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("data")

picture_model = api.model("picture_model", {
    'picture': fields.Boolean(required=True, description='Picture value')
})


@ns.route('/orders')
class DataOrderCollectionResource(Resource):
    
    @api.doc(security='apikey')
    @token_required
    @role_required(["DATA"])
    def get(self):

        dbo = app.order_dbo
        user = get_current_user()

        result = list()

        orders = dbo.read_all()

        for order in orders:
            if not dbo.verify_authority(order.id, user):
                continue

            if not order.research_completed:
                continue
                
            response = model_to_dict(order)

            response["assigned_date"] = str(response["assigned_date"])
            response["due_date"] = str(response["due_date"])
            
            response["state"]["state"] = order_states[response["state"]["state"]]

            result.append(response)

        return result


@ns.route('/orders/<int:_id>')
class DataOrderResource(Resource):
    
    @api.doc(security='apikey')
    @token_required
    @role_required(["DATA"])
    def get(self, _id):

        dbo = app.order_dbo
        user = get_current_user()

        if not dbo.verify_authority(_id, user):
            return 401, "Not authorized in this order"
        
        order = dbo.read(_id)

        response = model_to_dict(order)

        response["assigned_date"] = str(response["assigned_date"])
        response["due_date"] = str(response["due_date"])
        response["state"]["state"] = order_states[response["state"]["state"]]

        return response


@ns.route('/orders/<int:_id>/mark-completed')
class DataCompleteActionResource(Resource):
    
    @api.doc(security='apikey')
    @token_required
    @role_required(["DATA"])
    def post(self, _id):

        dbo = app.order_dbo
        user = get_current_user()

        if not dbo.verify_authority(_id, user):
            return 401, "Not authorized in this order"

        dbo.set_state(_id, "DATA_FINISH")

        order = dbo.read(_id)
        order.data_completed = True
        order.save()

        dbo = app.user_dbo

        users = dbo.read_all()

        for user in users:

            if user.role.role == "MANAGER" or user.role.role == "SUPERVISOR/MANAGER":

                send_mail_template("NOTIFY_MANAGER", order, username=user.username, from_email="admin@pams.com", to_emails=[user.email])
        
        return True

    
@ns.route('/orders/<int:_id>/mark-picture')
class DataMarkPictureResource(Resource):
    
    @api.doc(security='apikey')
    @token_required
    @role_required(["DATA"])
    def post(self, _id):

        dbo = app.order_dbo
        user = get_current_user()

        if not dbo.verify_authority(_id, user):
            return 401, "Not authorized in this order"

        dbo.mark_data_picture(_id)
        
        return True
