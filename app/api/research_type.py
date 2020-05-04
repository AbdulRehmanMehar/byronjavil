# -*- coding: utf-8 -*-
# app/api/research_type.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server

from .utils import token_required, role_required

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("admin")

research_type_model = api.model("research_type_model", {
    'type': fields.String(required=True, description='Research type')
})


@ns.route('/research-type')
class AdminResearchTypeCollectionResource(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def get(self):

        result = list()

        dbo = app.research_type_dbo

        research_types = dbo.read_all()

        for research_type in research_types:
            result.append(model_to_dict(research_type))

        return result

    @ns.expect(research_type_model)
    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def post(self):

        payload = api.payload

        _type = payload["type"]

        dbo = app.research_type_dbo

        research_type = dbo.create(_type)

        return model_to_dict(research_type)


@ns.route('/research-type/<int:_id>')
class AdminResearchTypeResource(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def get(self, _id):

        dbo = app.research_type_dbo

        research_type = dbo.read(_id)

        return model_to_dict(research_type)
    
    @ns.expect(research_type_model)
    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def put(self, _id):

        payload = api.payload

        _type = payload["type"]

        dbo = app.research_type_dbo

        dbo.update(_id, _type)

        return True

    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def delete(self, _id):

        dbo = app.research_type_dbo

        dbo.delete(_id)

        return True
