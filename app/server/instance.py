# -*- coding: utf-8 -*-
# app/server/instance.py

import os

from flask import Flask, Blueprint
from flask_login import LoginManager
from flask_restplus import Api, Namespace
from flask_peewee.db import Database

from peewee import SqliteDatabase, PostgresqlDatabase

from .dbo import *

# configure our database
DATABASE = {
    'name': '/var/www/property-management-system/id.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
SECRET_KEY = 'ssshhhh'
SENDGRID_API_KEY = "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"

authorizations = {
    'apikey' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'X-API-KEY'
    }
}

# database = SqliteDatabase(DATABASE["name"])


class API(Api):

    def __init__(self, *args, **kwargs):

        super(API, self).__init__(*args, **kwargs)

    def get_namespace(self, name):

        namespaces = self.namespaces

        for namespace in namespaces:

            if namespace.name == name:
                
                return namespace

def create_api(app):

    blueprint = Blueprint('api', __name__, url_prefix='/api')

    api = API(blueprint, version='1.0', 
            title='Property Management System API',
            description='A Flask API for Property Management System', 
            doc='/docs',
            authorizations=authorizations
        )

    app.register_blueprint(blueprint)

    ns_auth = Namespace('auth', description='Namespace for authentication')
    api.add_namespace(ns_auth, path='/auth')

    ns_admin = Namespace('admin', description='Namespace for admin')
    api.add_namespace(ns_admin, path='/admin')

    ns_supervisor = Namespace('supervisor', description='Namespace for supervisor')
    api.add_namespace(ns_supervisor, path='/supervisor')

    ns_company = Namespace('company', description='Namespace for company')
    api.add_namespace(ns_company, path='/company')

    ns_research = Namespace('research', description='Namespace for research')
    api.add_namespace(ns_research, path='/research')

    ns_data = Namespace('data', description='Namespace for data entry')
    api.add_namespace(ns_data, path='/data')

    ns_manager = Namespace('manager', description='Namespace for manager')
    api.add_namespace(ns_manager, path='/manager')

    ns_comment = Namespace('comment', description='Namespace for comment')
    api.add_namespace(ns_comment, path='/comment')

    ns_attachment = Namespace('attachment', description='Namespace for attachment')
    api.add_namespace(ns_attachment, path='/attachment')

    return api


class Server(object):
    
    def __init__(self):
    
        config_name = os.getenv('FLASK_CONFIG')

        if config_name == "development":

            self.app = Flask(__name__)
            self.app.config.from_object(__name__)
            self.database = SqliteDatabase(DATABASE["name"])

        elif config_name == "production":
    
            self.app = Flask(__name__)
            self.app.config.from_pyfile('config.py')

            database = self.app.config["DATABASE"]

            self.app.database = PostgresqlDatabase("PAMS", **database)
        
        # API

        self.api = create_api(self.app)

        # Database Objects

        self.app.user_dbo = UserDBO()
        self.app.attachment_dbo = AttachmentDBO()
        self.app.client_code_dbo = ClientCodeDBO()
        self.app.company_dbo = CompanyDBO()
        self.app.order_type_dbo = OrderTypeDBO()
        self.app.research_type_dbo = ResearchTypeDBO()
        self.app.order_dbo = OrderDBO()
        self.app.comment_dbo = CommentDBO()

        # Flask-Login

        self.app.login_manager = LoginManager()
        self.app.login_manager.init_app(self.app)
        self.app.login_manager.login_view = "auth.login"

        @self.app.before_request
        def before_request():
            try:
                self.app.database.connect()
            except:
                pass
        
        @self.app.after_request
        def after_request(response):
            try:
                self.app.database.close()
            except:
                pass
            return response

    def get_api(self):

        return self.api

    def get_app(self):

        return self.app

    def get_namespace(self, name):

        return self.api.get_namespace(name)

    def run(self):

        self.app.run()

server = Server()