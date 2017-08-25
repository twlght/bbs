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

main = Blueprint('index', __name__)


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form  # dict
    u = User.validate_login(form)
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('topic.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        log2(session)
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/user/<id>')  # 用id不重复
def user_detail(id):
    u = User.find_by_id(id)
    if u is None:
        abort(404)
    else:
        return render_template('profile.html', user=u)
        # abort(404)


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


@main.route('/add_img', methods=["POST"])
def add_img():
    file = request.files.get('file', None)
    # log2(request.files)
    # log2(type(file))
    # log2(file.filename)
    suffix = file.filename.split('.')[-1]
    # log2(suffix)
    if suffix in config.allowed_suffix:
        filename = '{}.{}'.format(uuid.uuid4(), suffix)
        u = current_user()
        u.filename = filename
        u.save()
        # log2(u.filename)
        file.save(os.path.join(config.users_img_directory, filename))
        return redirect(url_for('.profile'))
    else:
        abort(403)


@main.route('/upload/<filename>')
def upload(filename):
    return send_from_directory('users_img', filename)

