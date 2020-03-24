# -*- coding: utf-8 -*-
# app/models/models.py

"""models.py

This module implements classes for
modelling of the Property Management System API.
"""

import json
from datetime import datetime, date

from flask_restplus import fields
from peewee import Model, SqliteDatabase, TextField, FloatField, DateField, ForeignKeyField

db = SqliteDatabase("id.db")


class BaseModel(Model):

    class Meta:
        database = db


class UserRole(BaseModel):

    role = TextField()


class User(BaseModel):

    username = TextField()
    password = TextField()
    role = ForeignKeyField(UserRole)


class Authentication(BaseModel):

    user = ForeignKeyField(User)
    key = TextField()

    expire = DateField(default=date.today)


def reset():

    db.connect()

    models = [
        UserRole,
        User,
        Authentication
    ]

    db.drop_tables(models)
    db.create_tables(models)

    ROLES = ["SUPERVISOR", "RESEARCH", "DATA", "MANAGER"]

    for ROLE in ROLES:

        role =  UserRole.create(role=ROLE)
        role.save()
    
