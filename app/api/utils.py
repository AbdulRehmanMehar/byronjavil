# -*- coding: utf-8 -*-
# app/utils/auth.py

from functools import wraps

from flask import request

from app.server import server
from app.models import UserRole

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        app = server.get_app()
        dbo = app.user_dbo

        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        if not token:
            return {'message' : 'Key is missing.'}, 401

        if not dbo.verify_key(token):
            return {'message' : 'Invalid credentials!!!'}, 401
            
        return f(*args, **kwargs)

    return decorated

def role_required(f, role):
    @wraps(f)
    def decorated(*args, **kwargs):

        app = server.get_app()
        dbo = app.user_dbo

        token = request.headers['X-API-KEY']

        user = dbo.read_by_key(token)

        user_role = UserRole.select().where(UserRole.id==user.role_id).get()

        if not user_role.role == role:
            return {'message' : 'You are not authorized.'}, 401

        return f(*args, **kwargs)

    return decorated