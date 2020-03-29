# -*- coding: utf-8 -*-
# app/api/order_type.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server

from .utils import token_required, role_required

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("supervisor")

users_model = api.model("users_model", {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'email': fields.String(required=True, description='Email'),
    'role': fields.String(required=True, description='Role')
})


@ns.route('/users')
class SupervisorUsersCollection(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def get(self):

        result = list()

        dbo = app.user_dbo

        users = dbo.read_all()

        for user in users:

            user = model_to_dict(user)
            del user["password"]
            
            result.append(user)

        return result

    @ns.expect(users_model)
    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def post(self):

        payload = api.payload

        role = payload["role"]
        del payload["role"]

        dbo = app.user_dbo

        user = dbo.create(role, **payload)

        del user["password"]

        return model_to_dict(user)


@ns.route('/users/<username>')
class SupervisorUser(Resource):
    
    @ns.expect(users_model)
    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def put(self, username):

        payload = api.payload

        role = payload["role"]
        del payload["role"]

        dbo = app.user_dbo

        user = dbo.create(role, **payload)

        return model_to_dict(user)

    @api.doc(security='apikey')
    @token_required
    @role_required(["SUPERVISOR", "SUPERVISOR/MANAGER"])
    def delete(self, username):

        dbo = app.user_dbo

        dbo.delete(username)

        return True
