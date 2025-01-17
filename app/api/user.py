# -*- coding: utf-8 -*-
# app/api/order_type.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server

from .utils import token_required, role_required

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("admin")

users_model = api.model("users_model", {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'email': fields.String(required=True, description='Email'),
    'role': fields.String(required=True, description='Role')
})


@ns.route('/users')
class AdminUsersCollectionResource(Resource):

    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
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
    @role_required(["ADMIN"])
    def post(self):

        payload = api.payload

        role = payload["role"]
        del payload["role"]

        dbo = app.user_dbo

        user = dbo.create(role, **payload)
        
        response = model_to_dict(user)
        
        del response["password"]

        return response


@ns.route('/users/<username>')
class AdminUserResource(Resource):
    
    @ns.expect(users_model)
    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def put(self, username):

        payload = api.payload

        role = None
        
        try:
            role = payload["role"]
            del payload["role"]
        except:
            pass

        dbo = app.user_dbo

        payload["new_username"] = payload["username"]
        del payload["username"]
        del payload["password"]

        if role:

            dbo.update(username, role, **payload)
        
        else:

            dbo.update(username, **payload)


        return True

    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def delete(self, username):

        dbo = app.user_dbo

        dbo.delete(username)

        return True


change_password = api.model("change_password", {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})


@ns.route('/users/change-password')
class PasswordUserResource(Resource):
    
    @ns.expect(change_password)
    @api.doc(security='apikey')
    @token_required
    @role_required(["ADMIN"])
    def post(self):

        payload = api.payload

        username = payload["username"]
        password = payload["password"]

        dbo = app.user_dbo

        dbo.change_password(username, password)

        return True