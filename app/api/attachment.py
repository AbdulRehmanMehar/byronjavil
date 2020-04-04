# -*- coding: utf-8 -*-
# app/api/attachment.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server

from .utils import token_required, role_required, get_current_user

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("attachment")

upload_model = api.model("upload_model", {
    'filename': fields.String(required=True, description='File name'),
    'filetype': fields.String(required=True, description='File type'),
    'base64': fields.String(required=True, description='File base64')
})

@ns.route('/upload')
class UploadResource(Resource):

    @api.doc(security='apikey')
    @ns.expect(upload_model)
    @token_required
    @role_required(["SUPERVISOR", "RESEARCH"])
    def post(self):

        
        dbo = app.attachment_dbo

        payload = api.payload

        user = get_current_user()

        dbo.create(user, **payload)

        response = {
            "message": "File uploaded successfuly!"
        }

        return response


@ns.route('/order/<int_id>')
class OrderUploadResource(Resource):

    @api.doc(security='apikey')
    @ns.expect(upload_model)
    @token_required
    @role_required(["SUPERVISOR", "RESEARCH"])
    def post(self, _id):

        order_dbo = app.order_dbo
        attachment_dbo = app.attachment_dbo

        payload = api.payload

        user = get_current_user()
        order = order_dbo.read(_id)

        if not order_dbo.verify_authority(_id, user):
            return 401, "Not authorized in this order"

        attachment = attachment_dbo.create(user, **payload)
        attachment_dbo.append_to_order(attachment, order)

        response = {
            "message": "File uploaded successfuly!"
        }

        return response