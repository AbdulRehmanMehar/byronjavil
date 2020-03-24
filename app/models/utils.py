# -*- coding: utf-8 -*-
# app/models/utils.py

"""utils.py

This module implements functions for 
key generation and password verification.
"""

from uuid import uuid1
from hashlib import md5

def generate_key():

    return str(uuid1())

def hash_password(password):

    hash = md5(password.encode())

    return hash.hexdigest()

def verify_password(hash, password):

    return hash == hash_password(password)
