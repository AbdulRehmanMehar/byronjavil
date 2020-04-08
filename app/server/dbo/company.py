# -*- coding: utf-8 -*-
# app/server/dbo/company.py

from app.models import Company


class CompanyDBO:

    def create(self, **kwargs):
        
        customer = Company.create(**kwargs)

        return customer

    def read(self, _id):

        customer = Company.select().where(Company.id==_id).get()

        return customer

    def read_all(self):

        result = list()

        customers = Company.select()

        for customer in customers:

            result.append(customer)

        return result

    def update(self, _id, **kwargs):

        company = self.read(_id)

        for key, value in kwargs.items():

            setattr(company, key, value)

        company.save()
        
        return True

    def delete(self, _id):

        company = self.read(_id)

        company.delete_instance()

        return True
