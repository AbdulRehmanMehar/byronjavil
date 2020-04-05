# -*- coding: utf-8 -*-
# app/api/customer.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server

from .utils import token_required, role_required, get_current_user

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("comment")

comment_model = api.model("comment_model", {
    'text': fields.String(required=True, description='Comment Text')
})


@ns.route('/order/<int:_id>')
class OrderCommentCollectionResource(Resource):

    @api.doc(security='apikey')
    @token_required
    def get(self, _id):

        dbo = app.order_dbo
        user = get_current_user()

        if not dbo.verify_authority(_id, user):
            return 401, "Not authorized in this order"

        dbo = app.comment_dbo
        comments = dbo.read_by_order(_id)

        response = list()

        for comment in comments:

            comment = model_to_dict(comment)
            comment["created_date"] = str(comment["created_date"])

            response.append(comment)

        return response

    @api.doc(security='apikey')
    @token_required
    def post(self, _id):

        payload = api.payload

        text = payload["text"]

        order_dbo = app.order_dbo
        comment_dbo = app.comment_dbo

        user = get_current_user()
        order = order_dbo.read(_id)

        if not order_dbo.verify_authority(_id, user):
            return 401, "Not authorized in this order"

        comment = comment_dbo.create(user, text)
        comment_dbo.append_to_order(comment, order)

        return True