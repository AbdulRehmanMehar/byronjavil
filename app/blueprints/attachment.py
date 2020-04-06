# -*- coding: utf-8 -*-
# app/blueprints/attachment.py
import io
import base64

from flask import Response, send_file, render_template, redirect, url_for, request, session, abort, current_app
from flask_login import login_required, current_user

from . import attachment
from .utils import mime_types, file_types, role_required, InMemoryZipFile


@attachment.route('/attachment/<uuid>')
@login_required
def file(uuid):
    
    dbo = current_app.attachment_dbo

    attachment = dbo.read_by_uuid(uuid)

    filename = attachment.filename
    filetype = attachment.filetype

    filetype = file_types[filetype]

    filename += "." + filetype
    image_binary = base64.b64decode(attachment.base64)
    
    return send_file(
        io.BytesIO(image_binary),
        mimetype=mime_types[filetype],
        as_attachment=True,
        attachment_filename=filename
    )


@attachment.route('/attachment/<int:order_id>/download-all')
@login_required
def all_files(order_id):
    
    dbo = current_app.attachment_dbo

    attachments = dbo.read_by_order(order_id)

    zip_file = InMemoryZipFile()

    for attachment in attachments:

        filename = attachment.filename
        filetype = attachment.filetype

        filetype = file_types[filetype]

        filename += "." + filetype
        image_binary = base64.b64decode(attachment.base64)
        zip_file.write(filename, image_binary)
    
    return send_file(
        zip_file.get_zip(),
        mimetype="application/zip",
        as_attachment=True,
        attachment_filename="bundle.zip"
    )