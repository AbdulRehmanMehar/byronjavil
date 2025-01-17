# -*- coding: utf-8 -*-
# app/server/dbo/order.py

from app.models import OrderType, OrderState, OrderAttachment
from app.models import OrderComment, OrderPicture
from app.models import Order, Comment, Attachment


class OrderDBO:

    def create(self, **kwargs):

        order = Order.create(**kwargs)

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

    def update(self,  _id, **kwargs):

        order = self.read(_id)

        for key, value in kwargs.items():

            setattr(order, key, value)

        order.save()
        
        return True

    def delete(self, _id):

        order = self.read(_id)

        order.delete_instance()

    def verify_authority(self, _id, user):

        order = self.read(_id)

        if user.role.role in ["SUPERVISOR", "SUPERVISOR/MANAGER", "MANAGER"]:
            return True
        
        if (order.research_user == user) or (order.data_user == user):
            return True

        return False

    def verify_data(self, _id, user):

        order = self.read(_id)

        return order.research_id == user.id

    def set_state(self, _id, state):

        order = self.read(_id)
        order_state = OrderState.select().where(OrderState.state==state).get()

        order.state = order_state

        order.save()

        return True

    def mark_supervisor_picture(self, _id):

        order = self.read(_id)
        order.supervisor_picture = True

        order.save()

        return True

    def mark_data_picture(self, _id):

        self.set_state(_id, "MANAGEMENT")

        order = self.read(_id)
        order.data_picture = True
        order.data_completed = True

        order.save()

        return True

    def manager_submit(self, _id):

        order = self.read(_id)
        order.manager_submit = True
        
        order.save()

        self.set_state(_id, "FINISH")

        return True

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

    def delete_attachment(self, _id, attachment_id):

        order = self.read(_id)
        
        order_attachment = OrderAttachment.select().where(OrderAttachment.order_id==order.id).get()

        if order_attachment.attachment_id == attachment_id:

            order_attachment.delete_instance()

            return True

        return False


    def read_by_attachment(self, attachment_id):
        
        order_attachments = OrderAttachment.select()

        for order_attachment in order_attachments:

            if order_attachment.attachment_id == attachment_id:
                
                _id = order_attachment.order_id

        order = self.read(_id)

        return order