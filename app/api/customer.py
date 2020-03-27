# -*- coding: utf-8 -*-
# app/api/customer.py

from flask import request
from flask_restplus import Resource, fields
from playhouse.shortcuts import model_to_dict

from app.server import server

api = server.get_api()
app = server.get_app()
ns = server.get_namespace("supervisor")


@ns.route('/customers')
class SupervisorCustomerCollection(Resource):

    def get(self):

        result = list()

        dbo = app.customer_dbo

        customers = dbo.read_all()

        for customer in customers:
            result.append(model_to_dict(customer))

        return result

    def post(self):

        payload = api.payload

        dbo = app.customer_dbo

        customer = dbo.create(**payload)

        return model_to_dict(customer)


@ns.route('/customers/<int:_id>')
class SupervisorCustomer(Resource):

    def get(self, _id):

        dbo = app.customer_dbo

        customer = dbo.read(_id)

        return model_to_dict(customer)

    def put(self, _id):

        payload = api.payload

        dbo = app.customer_dbo

        dbo.update(_id, **payload)

        return True

    def delete(self, _id):

        dbo = app.customer_dbo

        dbo.delete(_id)

        return True
