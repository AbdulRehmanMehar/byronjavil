# -*- coding: utf-8 -*-
# app/server/dbo/order.py

from playhouse.shortcuts import model_to_dict

from app.models import Comment


class CommentDBO:

    def create(self, user, text):

        comment = Comment.create(text=text, user=user)

        return comment

    def read(self, _id):

        comment = Comment.select().where(Comment.id==_id).get()
        
        return comment

    def delete(self, _id):

        comment = self.read(_id)
        
        comment.delete_instance()

        return True

    def read_json(self, _id):

        comment = self.read(_id)
        comment = model_to_dict(comment)
        comment["created_date"] = str(comment["created_date"])

        return comment
