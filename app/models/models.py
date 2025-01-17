# -*- coding: utf-8 -*-
# app/models/models.py

"""models.py

This module implements classes for
modelling of the Property Management System API.
"""

import os

import json
from datetime import datetime, date

from flask import current_app
from flask_restplus import fields
from peewee import Model, SqliteDatabase, PostgresqlDatabase, TextField, BooleanField, BlobField, FloatField, DateField, DateTimeField, ForeignKeyField

# from app.server import server

# api = server.get_api()
config_name = os.getenv('FLASK_CONFIG')

if config_name == "development":
    db = SqliteDatabase("id.db")
else:
    database = {
        'user': 'postgres',
        'password': 'postgres',
        'host': '127.0.0.1',
        'port': 5432
    }

    db = PostgresqlDatabase("PAMS", **database)


class BaseModel(Model):

    class Meta:
        database = db


class UserRole(BaseModel):

    role = TextField()


class User(BaseModel):

    username = TextField()
    password = TextField()
    email = TextField()
    role = ForeignKeyField(UserRole)


class Authentication(BaseModel):

    user = ForeignKeyField(User)
    key = TextField()

    expire = DateField(default=date.today)


class ClientCode(BaseModel):

    code = TextField()


class Company(BaseModel):

    name = TextField()
    website = TextField()
    
    user = TextField()
    password = TextField()


class Comment(BaseModel):

    text = TextField()
    user = ForeignKeyField(User)

    created_date = DateTimeField(default=datetime.now)


class OrderType(BaseModel):

    order_type = TextField()


class OrderState(BaseModel):

    state = TextField()


class ResearchType(BaseModel):

    research_type = TextField()


class Order(BaseModel):

    address = TextField()

    full_address = TextField(default="")

    latitude = FloatField(default=0.0)
    longitude = FloatField(default=0.0)
    
    assigned_date = DateField(default=date.today)
    due_date = DateField(default=date.today)
    
    research_completed = BooleanField(default=False)
    data_completed = BooleanField(default=False)
    
    supervisor_picture = BooleanField(default=False)
    data_picture = BooleanField(default=False)
    manager_submit = BooleanField(default=False)

    company = ForeignKeyField(Company)
    research_user = ForeignKeyField(User, null=True)
    data_user = ForeignKeyField(User, null=True)

    client_code = ForeignKeyField(ClientCode)

    kind = ForeignKeyField(OrderType, null=True)
    research_type = ForeignKeyField(ResearchType, null=True)
    state = ForeignKeyField(OrderState, null=True)    
    

class Attachment(BaseModel):

    uuid = TextField()
    filename = TextField()
    filetype = TextField()

    base64 = BlobField()

    user = ForeignKeyField(User, null=True)

    created_date = DateTimeField(default=datetime.now)


class OrderComment(BaseModel):

    order = ForeignKeyField(column_name='order_id', field='id', model=Order)
    comment = ForeignKeyField(column_name='comment_id', field='id', model=Comment)


class OrderAttachment(BaseModel):

    order = ForeignKeyField(column_name='order_id', field='id', model=Order)
    attachment = ForeignKeyField(column_name='attachment_id', field='id', model=Attachment)


class OrderPicture(BaseModel):

    order = ForeignKeyField(column_name='order_id', field='id', model=Order)
    attachment = ForeignKeyField(column_name='attachment_id', field='id', model=Attachment)


class EmailTemplate(BaseModel):

    name = TextField()
    template = TextField()


def reset():

    from .utils import hash_password

    db.connect()

    models = [
        UserRole,
        User,
        Authentication,
        ClientCode,
        Company,
        Comment,
        OrderType,
        OrderState,
        ResearchType,
        Order,
        Attachment,
        OrderComment,
        OrderAttachment,
        OrderPicture,
        EmailTemplate
    ]

    db.drop_tables(models)
    db.create_tables(models)

    ROLES = ["ADMIN", "SUPERVISOR", "RESEARCH", "DATA", "MANAGER", "SUPERVISOR/MANAGER"]

    STATES = ["RESEARCH", "DATA_ENTRY", "DATA_FINISH", "MANAGEMENT", "FINISH", "ARCHIVE"]

    ORDER_TYPES = [
        "Exterior",
        "Exterior Inspection",
        "Exterior inspection across the view ",
        "Interior",
        "Interior inspection across the view"
    ]

    RESEARCH_TYPES = [
        "Normal",
        "High value",
        "High value and rental",
        "Less than z estimate",
        "Proximate"
    ]

    for ROLE in ROLES:

        UserRole.create(role=ROLE)

    for STATE in STATES:

        OrderState.create(state=STATE)

    for ORDER_TYPE in ORDER_TYPES:

        OrderType.create(order_type=ORDER_TYPE)

    for RESEARCH_TYPE in RESEARCH_TYPES:

        ResearchType.create(research_type=RESEARCH_TYPE)

    admin_role = UserRole.select().where(UserRole.role=="ADMIN").get()

    parameters = {
        "username": "admin",
        "password": "prosperity2020",
        "email": "admin@admin.com"
    }
    parameters["password"] = hash_password(parameters["password"])

    User.create(role_id=admin_role.id, **parameters)

    supervisor_role = UserRole.select().where(UserRole.role=="SUPERVISOR").get()

    parameters = {
        "username": "supervisor",
        "password": "prosperity2020",
        "email": "research@pams.com"
    }
    parameters["password"] = hash_password(parameters["password"])

    User.create(role_id=supervisor_role.id, **parameters)

    research_role = UserRole.select().where(UserRole.role=="RESEARCH").get()

    parameters = {
        "username": "research1",
        "password": "prosperity2020",
        "email": "research@pams.com"
    }
    parameters["password"] = hash_password(parameters["password"])

    User.create(role_id=research_role.id, **parameters)

    data_role = UserRole.select().where(UserRole.role=="DATA").get()

    parameters = {
        "username": "data1",
        "password": "prosperity2020",
        "email": "data@pams.com"
    }
    parameters["password"] = hash_password(parameters["password"])

    User.create(role_id=data_role.id, **parameters)

    data_role = UserRole.select().where(UserRole.role=="SUPERVISOR/MANAGER").get()

    parameters = {
        "username": "manager",
        "password": "prosperity2020",
        "email": "data@pams.com"
    }
    parameters["password"] = hash_password(parameters["password"])

    User.create(role_id=data_role.id, **parameters)
    