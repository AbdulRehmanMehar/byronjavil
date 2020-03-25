# -*- coding: utf-8 -*-
# app/blueprints/auth.py

# -*- coding: utf-8 -*-
# app/blueprints/auth.py

from flask import Response, render_template, redirect, url_for, request, session, abort, current_app
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

from . import auth

from app.server import server

app = server.get_app()


class User(UserMixin):

    def __init__(self, id):
        
        self.id = id


@auth.route('/login', methods=["GET", "POST"])
def login():

    """
    Render the login page
    """

    dbo = current_app.user_dbo

    if not request.method == 'POST':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    if not dbo.verify_username(username):
        return abort(401)
    
    if not dbo.login(username, password):

        return Response('''
        <b>
            Invalid credentials...
        </b>
        ''')

        
    user = dbo.read(username)
    user = User(user.id)
    login_user(user)
    
    _next = request.args.get("next")
    
    if not _next:
        return redirect(url_for("auth.home"))
    
    return redirect(_next)


@auth.route('/logout')
@login_required
def logout():

    """
    Render the logout page
    """
    from app.models import User

    user = User.select().where(User.id==current_user.id).get()

    dbo = current_app.user_dbo
    dbo.logout(user.username)

    logout_user()
    return Response('<p>Logged out</p>')


@auth.route('/home')
@login_required
def home():

    dbo = current_app.user_dbo

    user = dbo.read_by_id(current_user.id)

    return Response("Hello {}".format(user.username))


@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


@app.login_manager.user_loader
def load_user(userid):
    
    return User(userid)