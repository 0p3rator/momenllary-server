# -*- coding: UTF-8 -*- 
from flask import Blueprint, abort, request, redirect, Response, url_for
from service.forms import LoginForm
from service.user_service import User
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user
import os
import json


login_router = Blueprint('login_router',__name__)
login_router.secret_key = os.urandom(24)
# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
# login_manager.init_app(app=login_router)

# # csrf protection
# csrf = CsrfProtect()
# csrf.init_app(app)
# 这个callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def load_user(user_id):
    print "load_user"
    return User.get(user_id)

@login_router.route('/login', methods=['GET','POST'])
def login():
    print 1000
    form = LoginForm()
    print (form.validate_on_submit())
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        print user_name
        # remember_me = request.form.get('remember_me', False)
        user = User(user_name)
        if user.verify_password(password):
            login_user(user)
            return redirect(request.args.get('next') or url_for('sequences'))
            # return Response(json.dumps({'result':'true'}), status = 200, mimetype='application/json')
    return Response(json.dumps({'false':1}), status = 404, mimetype='application/json')


