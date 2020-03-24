# -*- coding: utf-8 -*-
# app/server/instance.py

from flask import Flask, Blueprint
from flask_restplus import Api, Namespace
from flask_peewee.db import Database

from peewee import SqliteDatabase

# configure our database
DATABASE = {
    'name': 'id.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
SECRET_KEY = 'ssshhhh'


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
            doc='/docs'
        )

    app.register_blueprint(blueprint)

    ns_auth = Namespace('auth', description='Namespace for authentication')
    api.add_namespace(ns_auth, path='/auth')

    ns_supervisor = Namespace('supervisor', description='Namespace for supervisor')
    api.add_namespace(ns_supervisor, path='/supervisor')

    ns_research = Namespace('research', description='Namespace for research')
    api.add_namespace(ns_research, path='/research')

    ns_data = Namespace('data', description='Namespace for data entry')
    api.add_namespace(ns_data, path='/data')

    ns_manager = Namespace('manager', description='Namespace for manager')
    api.add_namespace(ns_manager, path='/manager')

    ns_attachment = Namespace('attachment', description='Namespace for attachment')
    api.add_namespace(ns_attachment, path='/attachment')

    return api


class Server(object):
    
    def __init__(self):
    
        self.app = Flask(__name__)
        self.app.config.from_object(__name__)

        self.database = SqliteDatabase(DATABASE["name"])

        # from app.api import create_api
        
        self.api = create_api(self.app)

        @self.app.before_request
        def before_request():
            try:
                self.database.connect()
            except:
                pass
        
        @self.app.after_request
        def after_request(response):
            try:
                self.database.close()
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