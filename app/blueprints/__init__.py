# -*- coding: utf-8 -*-
# app/blueprints/__init__.py

from flask import Blueprint

from app.server import server

home = Blueprint('home', __name__)
auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)
supervisor = Blueprint('supervisor', __name__)
research = Blueprint('research', __name__)
data = Blueprint('data', __name__)
manager = Blueprint('manager', __name__)
attachment = Blueprint('attachment', __name__)

from .auth import *
from .admin import *
from .attachment import *
from .supervisor import *
from .research import *
from .data import *
from .manager import *
from .home import *

app = server.get_app()
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(supervisor)
app.register_blueprint(research)
app.register_blueprint(data)
app.register_blueprint(manager)
app.register_blueprint(attachment)
app.register_blueprint(home)
