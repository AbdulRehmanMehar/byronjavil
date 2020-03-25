# -*- coding: utf-8 -*-
# app/api/attachment.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server

from .utils import token_required

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("attachment")

upload_model = api.model("upload_model", {
    'filename': fields.String(required=True, description='File name'),
    'filetype': fields.String(required=True, description='File type'),
    'base64': fields.String(required=True, description='File base64')
})

@ns.route('/attachment')
class UploadResource(Resource):

    @ns.expect(upload_model)
    def post(self):

        dbo = app.attachment_dbo

        payload = api.payload

        dbo.create(**payload)

        response = {
            "message": "File uploaded successfuly!"
        }

        return response