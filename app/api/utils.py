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

def get_current_user():

    app = server.get_app()
    dbo = app.user_dbo

    token = request.headers['X-API-KEY']

    user = dbo.read_by_key(token)

    return user

def role_required(roles):
    
    def inner_function(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            app = server.get_app()
            dbo = app.user_dbo

            token = request.headers['X-API-KEY']

            user = dbo.read_by_key(token)

            user_role = UserRole.select().where(UserRole.id==user.role_id).get()

            if not user_role.role in roles:
                return {'message' : 'You are not authorized.'}, 401

            return f(*args, **kwargs)
        
        return decorated

    return inner_function

file_types = {
    "jpg": "jpg",
    "jpeg": "jpeg",
    "png": "png",
    "pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xls": "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "ppt": "application/vnd.ms-powerpoint",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "mp4": "video/mp4",
    "flv": "video/x-flv"
    
}

order_states = {
    "RESEARCH": "Under research",
    "DATA_ENTRY": "Pics not uploaded",
    "MANAGEMENT": "Ready to submit",
    "FINISH": "Submitted",
    "ARCHIVE": "Archived"
}