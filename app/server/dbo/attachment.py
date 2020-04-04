# -*- coding: utf-8 -*-
# app/server/dbo/__init__.py

from app.models import Attachment, OrderAttachment
from app.models import generate_key

class AttachmentDBO:

    def create(self, user, **kwargs):

        kwargs["uuid"] = generate_key()

        attachment = Attachment.create(user=user, **kwargs)

        return attachment

    def append_to_order(self, attachment, order):

        order_attachment = OrderAttachment.create(attachment=attachment, order=order)

        return order_attachment

    def read(self, _id):

        attachment = Attachment.select().where(Attachment.id==_id).get()

        return attachment

    def read_by_uuid(self, uuid):

        attachment = Attachment.select().where(Attachment.uuid==uuid).get()

        return attachment

    def delete(self, _id):

        attachment = Attachment.select().where(Attachment.id==_id).get()

        attachment.delete_instance()

        return True
