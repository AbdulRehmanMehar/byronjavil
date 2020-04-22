#!/usr/bin/python

import os
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/property-management-system/")

os.environ['FLASK_CONFIG'] = "production"

from run import server
application = server.app

# from FlaskApp import app as application
application.SECRET_KEY = 'ssshhhh'
