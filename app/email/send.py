# -*- coding: utf-8 -*-
# app/email/send.py

import os, jinja2
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, HtmlContent

from flask import render_template, request, url_for, current_app

from . import SENDGRID_API_KEY
from .messages import build_manager


def parse_template(username, message, url):
    response = render_template("email.html", username=username, message=message, url=url)
    return response

def send_mail(from_email, to_emails, subject, content):

    message = Mail(from_email=from_email, to_emails=To(to_emails), subject=subject, html_content=HtmlContent(content))
    
    try:
        api_key = current_app.config["SENDGRID_API_KEY"]
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
    except Exception as e:
        print(e)

def send_mail_template(template_code, order, **kwargs):

    manager = build_manager()

    message = manager.get(template_code)

    if template_code == "ASSIGN_RESEARCH":
        
        url = "http://{}{}".format(request.host, url_for("research.research_page"))
        message_content = message.message.format(order.address)
    
    if template_code == "ASSIGN_DATA":
        
        url = "http://{}{}".format(request.host, url_for("data.data_page"))
        message_content = message.message.format(order.address)
    
    if template_code == "NOTIFY_MANAGER":
        
        url = "http://{}{}".format(request.host, url_for("manager.manager_page"))
        message_content = message.message.format(order.address)

    username = kwargs["username"]

    from_email = kwargs["from_email"]
    to_emails = kwargs["to_emails"]
    subject = message.subject

    content = parse_template(username, message_content, url)
    send_mail(from_email, to_emails, subject, content)

