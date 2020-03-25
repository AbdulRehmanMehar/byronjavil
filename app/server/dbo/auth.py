# -*- coding: utf-8 -*-
# app/server/dbo/__init__.py

from app.models import User, UserRole, Authentication
from app.models import hash_password, verify_password, generate_key

class UserDBO:

    def create(self, role, **kwargs):

        role = UserRole.select().where(UserRole.role==role).get()

        kwargs["password"] = hash_password(kwargs["password"])

        user = User.create(role_id=role.id, **kwargs)

        return user

    def read(self, username):

        user = User.select().where(User.username==username).get()

        return user

    def read_by_id(self, _id):

        user = User.select().where(User.id==_id).get()

        return user

    def read_by_key(self, key):

        auth = Authentication.select().where(Authentication.key==key).get()

        user = User.select().where(User.id==auth.user_id).get()

        return user

    def update(self):

        pass

    def delete(self, username):

        user = User.select().where(User.username==username).get()

        user.delete_instance()
        
        return True

    def verify_username(self, username):

        try:
            User.select().where(User.username==username).get()
        except:
            return False
        
        return True

    def login(self, username, password):

        user = self.read(username)

        if verify_password(user.password, password):
            
            self._set_key(username)

            return True

        return False

    def logout(self, username):

        self._delete_key(username)

        return True
    
    def verify_key(self, key):

        try:
            auth = Authentication.select().where(Authentication.key==key).get()
            return True
        except:
            return False

    def _delete_key(self, key):

        try:
            auth = Authentication.select().where(Authentication.key==key).get()
            auth.delete_instance()
        except:
            pass

    def _set_key(self, username):

        user = self.read(username)
        key = generate_key()

        self._delete_key(username)

        Authentication.create(user_id=user.id, key=key)

    def _get_key(self, username):

        user = self.read(username)

        try:
            auth = Authentication.select().where(Authentication.user_id==user.id).get()
        except:
            return False

        return auth.key
