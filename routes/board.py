from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)
from routes import *
# from models.post import Topic
from models.board import Board
from utils import log2
'''
板块的添加属于管理员操作
topic页面显示所有版块
添加新
post
的时候, 需要选择板块
默认会给你选中当前板块
'''


main = Blueprint('board', __name__)


# @main.route("/")
# def index():
#     ms = Topic.all()
#     return render_template("post/index.html", ms=ms)


# @main.route('/<int:id>')
# def detail(id):
#     m = Topic.get(id)
#     # 传递 post 的所有 reply 到 页面中
#     return render_template("post/detail.html", post=m)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    # log2(form)
    cur_user = current_user()
    if cur_user.username == 'qwe':
        b = Board.new(form)
        return redirect(url_for('board.all'))
    else:
        return redirect(url_for('post.index'))


@main.route("/new")
def new():
    cur_user = current_user()
    return render_template("board/new.html", cur_user=cur_user)


@main.route("/all")
def all():
    cur_user = current_user()
    bs = Board.all()
    return render_template("board/all.html", boards=bs, cur_user=cur_user)
