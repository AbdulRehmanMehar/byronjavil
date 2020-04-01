# -*- coding: utf-8 -*-
# app/server/dbo/order.py

from app.models import OrderType, OrderState, OrderAttachment
from app.models import OrderComment, OrderPicture
from app.models import Order, Comment, Attachment


class OrderDBO:

    def create(self, user, customer, **kwargs):

        order = Order.create(user=user, customer=customer, **kwargs)

        return order

    def read(self, _id):

        order = Order.select().where(Order.id==_id).get()

        return order

    def read_all(self):

        result = list()

        orders = Order.select()

        for order in orders:

            result.append(order)

        return result

    def update(self, _id):

        pass

    def delete(self, _id):

        order = self.read(_id)

        order.delete_instance()

    def assign_user(self, user):

        pass
    
    def set_state(self, _id, state):

        pass

    def set_type(self, _id, _type):

        pass

    def append_comment(self, _id, user, comment):
        
        order = self.read(_id)

        comment = Comment.create(user=user, text=comment)
        OrderComment.create(order=order, comment=comment)

        return True

    def get_comments(self, _id):

        result = list()

        order = self.read(_id)
        
        order_comments = OrderComment.select().where(OrderComment.order_id==order.id).get()

        for order_comment in order_comments:

            comment = Comment.select().where(Comment.id==order_comment.comment_id).get()

            result.append(comment)

        return result

    def append_attachment(self, _id, attachment):

        order = self.read(_id)

        OrderAttachment.create(order=order, attachment=attachment)

        return True

    def get_attachments(self, _id):

        result = list()

        order = self.read(_id)
        
        order_attachments = OrderAttachment.select().where(OrderAttachment.order_id==order.id).get()

        for order_attachment in order_attachments:

            attachment = Attachment.select().where(Attachment.id==order_attachment.attachment_id).get()

            result.append(attachment)

        return result