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
from models.post import Post
from models.board import Board
from utils import log, log2
import uuid
import os
import config.config as config
from config.config import topics_per_page
from routes import current_user
from bson.objectid import ObjectId
import json

main = Blueprint('index', __name__)
# csrf_token = dict()


@main.route("/")
def index():
    board_id = request.args.get('board_id', '-1')
    page = int(request.args.get('page', 1))
    cur_user = current_user()
    if board_id == '-1':
        ts = Post.all()
    else:
        ts = Post.find_all(board_id=board_id)
    max_page = int(len(ts) / topics_per_page + 1)
    if page > max_page:
        return redirect(url_for('.index', page=max_page, board_id=board_id))
    if page == max_page:
        ts = ts[(page-1) * topics_per_page:]
    else:
        ts = ts[(page-1) * topics_per_page:page * topics_per_page]
    token = str(uuid.uuid4())
    session['token'] = token
    bs = Board.all()
    return render_template("index.html",
                           page=page, max_page=max_page, ts=ts, token=token,
                           bs=bs, board_id=board_id, cur_user=cur_user)


@main.route('/user/<id>')  # 用id不重复
def user_detail(id):
    cur_user = current_user()
    u = User.find_by_id(id)
    if u is None:
        abort(404)
    else:
        ts = u.topics()
        return render_template('user_detail.html', cur_user=cur_user, user=u, ts=ts)


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


@main.route('/axios_test')
def axios_test():
    js = request.headers
    print(js)
    boards = ['python', 'linux', 'vue', 'mongodb', 'nginx']
    return json.dumps(boards)
