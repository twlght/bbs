from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *

# from models.topic import Topic
from models.board import Board
from utils import log2

main = Blueprint('board', __name__)


# @main.route("/")
# def index():
#     ms = Topic.all()
#     return render_template("topic/index.html", ms=ms)


# @main.route('/<int:id>')
# def detail(id):
#     m = Topic.get(id)
#     # 传递 topic 的所有 reply 到 页面中
#     return render_template("topic/detail.html", topic=m)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    log2(form)
    u = current_user()
    if u.id == 6:
        b = Board.new(form)
        return redirect(url_for('board.all'))
    else:
        return redirect(url_for('topic.index'))


@main.route("/new")
def new():
    return render_template("board/new.html")


@main.route("/all")
def all():
    bs = Board.all()
    return render_template("board/all.html", boards=bs)