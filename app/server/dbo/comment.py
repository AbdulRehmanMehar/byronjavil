# -*- coding: utf-8 -*-
# app/server/dbo/order.py

from playhouse.shortcuts import model_to_dict

from app.models import Comment, OrderComment


class CommentDBO:

    def create(self, user, text):

        comment = Comment.create(text=text, user=user)

        return comment

    def append_to_order(self, comment, order):

        order_comment = OrderComment.create(comment=comment, order=order)
        
        return order_comment

    def read(self, _id):

        comment = Comment.select().where(Comment.id==_id).get()
        
        return comment

    def delete(self, _id):

        comment = self.read(_id)
        
        comment.delete_instance()

        return True

    def read_by_order(self, order_id):

        result = list()

        order_comments = OrderComment.select().where(OrderComment.order_id==order_id)

        for order_comment in order_comments:

            comment = Comment.select().where(Comment.id==order_comment.comment_id).get()

            result.append(comment)

        return result

    def read_json(self, _id):

        comment = self.read(_id)
        comment = model_to_dict(comment)
        comment["created_date"] = str(comment["created_date"])

        return comment
