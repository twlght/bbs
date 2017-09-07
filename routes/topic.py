from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)
from routes import *
from models.topic import Topic
from models.board import Board
from utils import log2
import uuid


main = Blueprint('topic', __name__)
csrf_token = dict()


@main.route('/<id>')
def detail(id):
    topic = Topic.get(id)
    cur_user = current_user()
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=topic, cur_user=cur_user)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    # log2('type of token:', type(request.args.get('token')))  # type of token: <class 'str'>
    log2(form)
    token = request.args.get('token')
    if csrf_token['token'] == token:
        u = current_user()
        m = Topic.new(form, user_id=u.id)
        return redirect(url_for('.detail', id=m.id))
    else:
        abort(403)


@main.route("/new")
def new():
    token = str(uuid.uuid4())
    csrf_token['token'] = token
    # log2(csrf_token)
    bs = Board.all()
    return render_template("topic/new.html", boards=bs, token=token)


@main.route("/delete")
def delete():
    id = request.args.get('id')
    token = request.args.get('token')
    if csrf_token['token'] == token:
        Topic.delete(id=id)
        return redirect(url_for('.index'))
    else:
        abort(403)

