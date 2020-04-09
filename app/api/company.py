# -*- coding: utf-8 -*-
# app/api/company.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server

from .utils import token_required, role_required

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("admin")

company_model = api.model("company_model", {
    'company': fields.String(required=True, description='Company name'),
    'website': fields.String(required=True, description='Company website'),
    'user': fields.String(required=True, description='Company user'),
    'password': fields.String(required=True, description='Company password')
})


@ns.route('/companies')
class AdminCompanyCollectionResource(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def get(self):

        result = list()

        dbo = app.company_dbo

        companies = dbo.read_all()

        for company in companies:
            result.append(model_to_dict(company))

        return result

    @ns.expect(company_model)
    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def post(self):

        payload = api.payload

        dbo = app.company_dbo

        company = dbo.create(**payload)

        return model_to_dict(company)


@ns.route('/companies/<int:_id>')
class AdminCompanyResource(Resource):
    
    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def get(self, _id):

        dbo = app.company_dbo

        company = dbo.read(_id)

        return model_to_dict(company)

    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def put(self, _id):

        payload = api.payload

        dbo = app.company_dbo
        client_dbo = app.client_code_dbo

        client_code = client_dbo.read_by_code(payload["client_code"])
        payload["client_code"] = client_code

        dbo.update(_id, **payload)

        return True

    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def delete(self, _id):

        dbo = app.company_dbo

        dbo.delete(_id)

        return True
