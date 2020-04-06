# app/email/send.py

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from . import SENDGRID_API_KEY

def send_mail(from_email, to_emails, subject, content):

    message = Mail(from_email=from_email, to_emails=to_emails, subject=subject, html_content=content)
    
    try:
        sg = SendGridAPIClient('SENDGRID_API_KEY')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
