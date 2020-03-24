# -*- coding: utf-8 -*-
# app/server/dbo/__init__.py

from app.models import User, UserRole, Authentication
from app.models import hash_password, verify_password

class UserDBO:

    def create(self, role, **kwargs):

        role = UserRole.select().where(UserRole.role==role).get()

        kwargs["password"] = hash_password(kwargs["password"])

        user = User.create(role_id=role.id, **kwargs)

        return user

    def read(self, username):

        user = User.select().where(User.username==username).get()

        return user

    def update(self):

        pass

    def delete(self, username):

        user = User.select().where(User.username==username).get()

        user.delete_instance()
        
        return True

    def verify_username(self, username):

        try:
            user = User.select().where(User.username==username).get()
        except:
            return False
        
        return True

    def login(self, username, password):

        user = self.read(username)

        if verify_password(user.password, password):

            return True

        return False

    def logout(self, username):

        return True