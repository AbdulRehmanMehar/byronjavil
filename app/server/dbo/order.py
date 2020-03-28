# -*- coding: utf-8 -*-
# app/server/dbo/order.py

from app.models import OrderType, OrderState, OrderAttachment
from app.models import OrderComment, OrderPicture
from app.models import Order


class OrderDBO:

    def create(self):

        pass

    def read(self, _id):

        pass

    def read_all(self):

        pass

    def update(self, _id):

        pass

    def delete(self, _id):

        pass

    def assign_user(self, user):

        pass
    
    def set_state(self, _id, state):

        pass

    def append_comment(self, comment):

        pass

    def get_comments(self, _id):

        pass

    def append_attachment(self, attachment):

        pass

    def get_attachments(self, _id):

        pass