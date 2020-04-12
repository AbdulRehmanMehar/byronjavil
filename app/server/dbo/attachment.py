# -*- coding: utf-8 -*-
# app/server/dbo/attachment.py

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

    def read_by_order(self, order_id):
        
        result = list()

        order_attachments = OrderAttachment.select().where(OrderAttachment.order_id==order_id)

        for order_attachment in order_attachments:

            attachment = Attachment.select().where(Attachment.id==order_attachment.attachment_id).get()

            result.append(attachment)

        return result

    def delete(self, _id):

        attachment = Attachment.select().where(Attachment.id==_id).get()

        attachment.delete_instance()

        return True
