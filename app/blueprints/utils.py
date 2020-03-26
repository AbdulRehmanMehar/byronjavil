# -*- coding: utf-8 -*-
# app/blueprints/utils.py

from functools import wraps

from flask import request, render_template

from app.server import server
from app.models import UserRole


mime_types = {
    "jpg": "image/jpeg",
    "png": "image/png",
    "pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "ppt": "application/vnd.ms-powerpoint",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "mp4": "video/mp4",
    "flv": "video/x-flv"
    
}

def render_message(message, description):
    
    return render_template("message.html", message=message, description=description)

def role_required(role):
    
    def inner_function(f):
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

    return inner_function