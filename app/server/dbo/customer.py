# -*- coding: utf-8 -*-
# app/server/dbo/customer.py

from app.models import Customer


class CUstomerDBO:

    def create(self, **kwargs):
        
        customer = Customer.create(**kwargs)

        return customer

    def read(self, _id):

        customer = Customer.select().where(Customer.id==_id).get()

        return customer

    def update(self, _id, **kwargs):

        customer = self.read(_id)

        for key, value in kwargs.items():

            setattr(customer, key, value)

        customer.save()
        
        return True

    def delete(self, _id):

        customer = self.read(_id)

        customer.delete_instance()

        return True
