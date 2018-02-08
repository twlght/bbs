from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory
)

from models.user import User
from utils import log, log2
import uuid
import os
import config.config as config
from routes import current_user
from bson.objectid import ObjectId

main = Blueprint('auth', __name__)


@main.route("/register", methods=['GET','POST'])
def register():
    form = request.form
    if form != {}:
        u = User.register(form)
        return redirect(url_for('index.index'))
    # 用类函数来判断
    return render_template('auth/register.html')


@main.route("/login", methods=['GET', 'POST'])
def login():
    form = request.form  # dict
    if form != {}:
        u = User.validate_login(form)
        if u is None:
            return redirect(url_for('index.index'))
        else:
            # session 中写入 user_id
            session['user_id'] = u.id
            # log2(session)
            # 设置 cookie 有效期为 永久
            session.permanent = True
            return redirect(url_for('index.index'))
    return render_template('auth/login.html')


@main.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id')
    return redirect(url_for('index.index'))


@main.route('/search_password', methods=['GET', 'POST'])
def search_password():
    pass

