# -*- coding: utf-8 -*-
# app/blueprints/auth.py

from flask import Response, render_template, redirect, url_for, request, session, abort, current_app
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

from . import auth
from .utils import render_message, role_required, get_current_role

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
        if current_user.is_authenticated:

            role = get_current_role()

            if role == "SUPERVISOR/MANAGER":
                return redirect(url_for('auth.supervisor_manager'))
            elif role == "SUPERVISOR":
                return redirect(url_for('supervisor.supervisor_page'))
            elif role == "MANAGER":
                return redirect(url_for('manager.manager_page'))
            elif role == "RESEARCH":
                return redirect(url_for('research.research_page'))
            elif role == "DATA":
                return redirect(url_for('data.data_page'))

            return redirect(url_for("auth.home"))

        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    if not dbo.verify_username(username):
        return abort(401)
    
    if not dbo.login(username, password):

        message = "Login failed"
        description = "Invalid credentials"

        return render_message(message, description)

        
    user = dbo.read(username)
    user = User(user.id)
    login_user(user)
    
    _next = request.args.get("next")
    
    if not _next:
        role = dbo.get_role(username)

        if role == "SUPERVISOR/MANAGER":
            return redirect(url_for('auth.supervisor_manager'))
        elif role == "SUPERVISOR":
            return redirect(url_for('supervisor.supervisor_page'))
        elif role == "MANAGER":
            return redirect(url_for('manager.manager_page'))
        elif role == "RESEARCH":
            return redirect(url_for('research.research_page'))
        elif role == "DATA":
            return redirect(url_for('data.data_page'))
        
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

    message = "Logged out successfuly"
    description = "You have been logout from Property Addresses Managament System"
    
    return render_message(message, description)


@app.errorhandler(401)
def page_not_found(e):

    message = "Login failed"
    description = "Invalid credentials"

    return render_message(message, description)


@app.login_manager.user_loader
def load_user(userid):
    
    return User(userid)


@auth.route('/supervisor-manager')
@login_required
@role_required(["SUPERVISOR/MANAGER"])
def supervisor_manager():

    dbo = current_app.user_dbo

    user = dbo.read_by_id(current_user.id)
    
    return render_template("supervisor_manager.html")