# -*- coding: utf-8 -*-
# app/models/models.py

"""models.py

This module implements classes for
modelling of the Property Management System API.
"""

import json
from datetime import datetime, date

from flask_restplus import fields
from peewee import Model, SqliteDatabase, TextField, BlobField, FloatField, DateField, DateTimeField, ForeignKeyField

db = SqliteDatabase("id.db")


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


class Customer(BaseModel):

    company = TextField()
    client_code = TextField()
    website = TextField()
    
    user = TextField()
    password = TextField()


class Comment(BaseModel):

    text = TextField()
    user = ForeignKeyField(User)


class OrderType(BaseModel):

    order_type = TextField()


class OrderState(BaseModel):

    state = TextField()


class Order(BaseModel):

    address = TextField()
    
    date_assigned = DateField(default=date.today)
    due_date = DateField(default=date.today)
    
    company = ForeignKeyField(Customer)
    user = ForeignKeyField(User)
    
    kind = ForeignKeyField(OrderType)
    state = ForeignKeyField(OrderState)
    

class Attachment(BaseModel):

    uuid = TextField()
    filename = TextField()
    filetype = TextField()

    base64 = BlobField()


class OrderComment(BaseModel):

    order = ForeignKeyField(column_name='research_id', field='id', model=Order)
    comment = ForeignKeyField(column_name='comment_id', field='id', model=Comment)


class OrderAttachment(BaseModel):

    order = ForeignKeyField(column_name='research_id', field='id', model=Order)
    attachment = ForeignKeyField(column_name='attachment_id', field='id', model=Attachment)


class OrderPicture(BaseModel):

    order = ForeignKeyField(column_name='research_id', field='id', model=Order)
    attachment = ForeignKeyField(column_name='attachment_id', field='id', model=Attachment)


class EmailTemplate(BaseModel):

    name = TextField()
    template = TextField()


def reset():

    db.connect()

    models = [
        UserRole,
        User,
        Authentication,
        Customer,
        Comment,
        OrderType,
        OrderState,
        Order,
        Attachment,
        OrderComment,
        OrderAttachment,
        OrderPicture,
        EmailTemplate
    ]

    db.drop_tables(models)
    db.create_tables(models)

    ROLES = ["SUPERVISOR", "RESEARCH", "DATA", "MANAGER", "SUPERVISOR/MANAGER"]

    for ROLE in ROLES:

        role =  UserRole.create(role=ROLE)
        role.save()
    
