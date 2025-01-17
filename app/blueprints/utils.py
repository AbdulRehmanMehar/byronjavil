# -*- coding: utf-8 -*-
# app/blueprints/utils.py

import io

from zipfile import ZipFile
from functools import wraps

from flask import request, render_template, current_app
from flask_login import current_user

from app.server import server
from app.models import UserRole


mime_types = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "pdf": "application/pdf",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "ppt": "application/vnd.ms-powerpoint",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "mp4": "video/mp4",
    "flv": "video/x-flv"
    
}

file_types = {
    "jpg": "jpg",
    "jpeg": "jpeg",
    "png": "png",
    "gif": "gif",
    "pdf": "pdf",
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

def render_message(message, description):
    
    return render_template("message.html", message=message, description=description)

def role_required(roles):
    
    def inner_function(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            app = server.get_app()
            dbo = app.user_dbo

            user = dbo.read_by_id(current_user.id)

            user_role = UserRole.select().where(UserRole.id==user.role_id).get()

            if not user_role.role in roles:
                message = "Unauthorized"
                description = "You do not have authorization to enter this page"
                
                return render_message(message, description)

            return f(*args, **kwargs)
        
        return decorated

    return inner_function

def get_current_role():

    dbo = current_app.user_dbo

    user = dbo.read_by_id(current_user.id)

    return user.role.role
    
def get_credentials():

    dbo = current_app.user_dbo

    user = dbo.read_by_id(current_user.id)

    key = dbo._get_key(user.username)

    credentials = {
        "username": user.username,
        "role": user.role.role,
        "api-key": key
    }

    return credentials

from random import randint

class InMemoryZipFile(object):
    
    def __init__(self):
        
        self.inMemoryOutputFile = io.BytesIO()

    def write(self, inzipfilename, data):
        
        zip = ZipFile(self.inMemoryOutputFile, 'a')
        zip.writestr(inzipfilename, data)
        zip.close()

    def get_zip(self):
        self.inMemoryOutputFile.seek(0)
        return self.inMemoryOutputFile
    
    def read(self):
        
        self.inMemoryOutputFile.seek(0)
        return self.inMemoryOutputFile.getvalue()