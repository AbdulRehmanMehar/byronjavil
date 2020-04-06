# -*- coding: utf-8 -*-
# app/api/data.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server
from app.models import OrderState, OrderType, OrderPicture

from .utils import token_required, role_required, get_current_user

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

        response = list()

        orders = dbo.read_all()

        for order in orders:
            if dbo.verify_authority(order.id, user):
                
                result = model_to_dict(order)

                result["date_assigned"] = str(result["date_assigned"])
                result["due_date"] = str(result["due_date"])

                response.append(result)

        return response


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

        response["date_assigned"] = str(response["date_assigned"])
        response["due_date"] = str(response["due_date"])

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

        dbo.set_state(_id, "MANAGEMENT")

        order = dbo.read(_id)
        order.data_completed = True
        order.save()

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

        dbo.mark_picture(_id)
        
        return True
