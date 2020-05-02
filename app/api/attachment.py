# -*- coding: utf-8 -*-
# app/api/attachment.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server

from .utils import token_required, role_required, get_current_user, file_types

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


@ns.route('/order/<int:_id>')
class OrderUploadResource(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "RESEARCH", "DATA", "MANAGER", "SUPERVISOR/MANAGER"])
    def get(self, _id):

        order_dbo = app.order_dbo
        attachment_dbo = app.attachment_dbo

        user = get_current_user()

        if not order_dbo.verify_authority(_id, user):
            return 401, "Not authorized in this order"

        response = list()

        attachments = attachment_dbo.read_by_order(_id)

        for attachment in attachments:

            filetype = file_types[attachment.filetype]

            result = {
                "uuid": attachment.uuid,
                "filename": attachment.filename,
                "filetype": filetype,
                "username": attachment.user.username,
                "userrole": attachment.user.role.role,
                "created_date": str(attachment.created_date),
                "url": "/attachment/" + attachment.uuid
            }

            response.append(result)

        return response
    
    @api.doc(security='apikey')
    @ns.expect(upload_model)
    @token_required
    @role_required(["SUPERVISOR", "RESEARCH", "DATA"])
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


@ns.route('/delete/<uuid>')
class DeleteResource(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "RESEARCH", "DATA", "MANAGER", "SUPERVISOR/MANAGER"])
    def delete(self, uuid):

        order_dbo = app.order_dbo
        attachment_dbo = app.attachment_dbo

        user = get_current_user()
        attachment = attachment_dbo.read_by_uuid(uuid)
        owner = attachment_dbo.get_owner(attachment.id)

        if not user.username == owner.username:

            if not user.role.role in ["ADMIN"]:
                return 401, "Not authorized to delete this file"

        order = order_dbo.read_by_attachment(attachment.id)
        
        if order_dbo.delete_attachment(order.id, attachment.id):
            attachment_dbo.delete(attachment.id)

        return 200, "File successfully deleted"
        