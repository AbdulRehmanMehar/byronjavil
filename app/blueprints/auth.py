# -*- coding: utf-8 -*-
# app/blueprints/auth.py

# -*- coding: utf-8 -*-
# app/blueprints/auth.py

from flask import Response, render_template, redirect, url_for, request, session, abort, current_app
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 

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

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(username, password)

        if dbo.verify_username(username):
            if dbo.login(username, password):
                
                user = dbo.read(username)
                user = User(user.id)
                login_user(user)
                
                _next = request.args.get("next")
                
                if _next:

                    return redirect(_next)

                else:
                    return redirect(url_for("auth.home"))
            else:
                return Response('''
                <b>
                    Invalid credentials...
                </b>
                ''')

        else:
            return abort(401)
    
    else:
        return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():

    """
    Render the logout page
    """
    logout_user()
    return Response('<p>Logged out</p>')


@auth.route('/home')
@login_required
def home():
    return Response("Hello World!")

@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


@app.login_manager.user_loader
def load_user(userid):
    return User(userid)