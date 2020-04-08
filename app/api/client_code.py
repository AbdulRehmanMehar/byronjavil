# -*- coding: utf-8 -*-
# app/api/client.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server

from .utils import token_required, role_required

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("admin")

client_code_model = api.model("client_code_model", {
    'code': fields.String(required=True, description='Client Code')
})


@ns.route('/client-code')
class AdminClientCodeCollectionResource(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def get(self):

        result = list()

        dbo = app.client_code_dbo

        client_codes = dbo.read_all()

        for client_code in client_codes:
            result.append(model_to_dict(client_code))

        return result

    @ns.expect(client_code_model)
    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def post(self):

        payload = api.payload

        code = payload["code"]

        dbo = app.client_code_dbo

        client_code = dbo.create(code)

        return model_to_dict(client_code)


@ns.route('/client-code/<int:_id>')
class AdminOrderTypeResource(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def get(self, _id):

        dbo = app.client_code_dbo

        client_code = dbo.read(_id)

        return model_to_dict(client_code)
    
    @ns.expect(client_code_model)
    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def put(self, _id):

        payload = api.payload

        code = payload["code"]

        dbo = app.client_code_dbo

        dbo.update(_id, code)

        return True

    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def delete(self, _id):

        dbo = app.client_code_dbo

        dbo.delete(_id)

        return True
