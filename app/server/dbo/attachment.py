# -*- coding: utf-8 -*-
# app/server/dbo/__init__.py

from app.models import Attachment


class AttachmentDBO:

    def create(self, **kwargs):

        attachment = Attachment.create(**kwargs)

        return attachment

    def read(self, _id):

        attachment = Attachment.select().where(Attachment.id==_id).get()

        return attachment

    def delete(self, _id):

        attachment = Attachment.select().where(Attachment.id==_id).get()

        attachment.delete_instance()

        return True
        