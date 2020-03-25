# -*- coding: utf-8 -*-
# app/models/models.py

"""models.py

This module implements classes for
modelling of the Property Management System API.
"""

import json
from datetime import datetime, date

from flask_restplus import fields
from peewee import Model, SqliteDatabase, TextField, BlobField, FloatField, DateField, ForeignKeyField

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
    
    user = ForeignKeyField(User)

class Comment(BaseModel):

    text = TextField()
    user = ForeignKeyField(User)


class ResearchState(BaseModel):

    state = TextField()


class Research(BaseModel):

    state = ForeignKeyField(ResearchState)
    

class Attachment(BaseModel):

    uuid = TextField()
    filename = TextField()
    filetype = TextField()

    base64 = BlobField()


def reset():

    db.connect()

    models = [
        UserRole,
        User,
        Authentication,
        Attachment
    ]

    db.drop_tables(models)
    db.create_tables(models)

    ROLES = ["SUPERVISOR", "RESEARCH", "DATA", "MANAGER"]

    for ROLE in ROLES:

        role =  UserRole.create(role=ROLE)
        role.save()
    
