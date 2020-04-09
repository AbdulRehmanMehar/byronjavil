# -*- coding: utf-8 -*-
# app/server/dbo/company.py

from app.models import Company


class CompanyDBO:

    def create(self, **kwargs):
        
        company = Company.create(**kwargs)

        return company

    def read(self, _id):

        company = Company.select().where(Company.id==_id).get()

        return company

    def read_all(self):

        result = list()

        companies = Company.select()

        for company in companies:

            result.append(company)

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
