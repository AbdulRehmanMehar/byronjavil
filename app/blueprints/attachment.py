# -*- coding: utf-8 -*-
# app/blueprints/attachment.py
import io
import base64

from flask import Response, send_file, render_template, redirect, url_for, request, session, abort, current_app
from flask_login import login_required, current_user

from . import attachment
from .utils import mime_types


@attachment.route('/attachment/<uuid>')
def file(uuid):
    
    dbo = current_app.attachment_dbo

    attachment = dbo.read_by_uuid(uuid)

    filename = attachment.filename
    filetype = attachment.filetype

    filename += "." + attachment.filetype
    image_binary = base64.b64decode(attachment.base64)

    return send_file(
        io.BytesIO(image_binary),
        mimetype=mime_types[filetype],
        as_attachment=True,
        attachment_filename=filename
    )