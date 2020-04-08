# -*- coding: utf-8 -*-
# app/server/dbo/client_code.py

from app.models import ClientCode


class ClientCodeDBO:

    def create(self, code):

        client_code = ClientCode.create(client_code=code)

        return client_code

    def read(self, _id):

        client_code = ClientCode.select().where(ClientCode.id==_id).get()

        return client_code

    def read_by_code(self, code):

        client_code = ClientCode.select().where(ClientCode.code==code).get()

        return client_code

    def read_all(self):

        result = list()

        client_codes = ClientCode.select()

        for client_code in client_codes:
            result.append(client_code)
        
        return result

    def update(self, _id, code):

        client_code = self.read(_id)

        client_code.code = code
        client_code.save()

        return True

    def delete(self, _id):

        client_code = self.read(_id)
        client_code.delete_instance()

        return True


