# -*- coding: utf-8 -*-
# app/server/dbo/order_type.py

from app.models import OrderType


class OrderTypeDBO:

    def create(self, _type):

        order_type = OrderType.create(order_type=_type)

        return order_type

    def read(self, _id):

        order_type = OrderType.select().where(OrderType.id==_id).get()

        return order_type

    def read_by_type(self, _type):

        order_type = OrderType.select().where(OrderType.order_type==_type).get()

        return order_type

    def read_all(self):

        result = list()

        order_types = OrderType.select()

        for order_type in order_types:
            result.append(order_type)
        
        return result

    def update(self, _id, _type):

        order_type = self.read(_id)

        order_type.order_type = _type
        order_type.save()

        return True

    def delete(self, _id):

        order_type = self.read(_id)

        order_type.delete_instance()

        return True


