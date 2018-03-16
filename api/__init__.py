import json
from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory,
    jsonify,
)
from models.user import User
from models.post import Post
from models.board import Board

main = Blueprint('api', __name__)
"""
请求中包含的json数据可通过request.json获取,
并且需要包含json的响应可以使用flask提供的辅助函数jsonify()从python字典中生成,
或者用json.dumps()生成;
jsonify与json.dumps的区别在于响应headers中的Content-Type不同:
jsonify: Content-Type: application/json
json.dumps: Content-Type: text/html; charset=utf-8
json是http请求和响应使用的传输格式;

书上的做法是db的数据通过orm生成实例, 再将实例通过to_json()变成json格式的数据;
api:
/boards: 所有版块名及信息;

/posts: 所有文章;
/posts/<str: id>: 一篇文章;
/posts/<str: id>/comments: 一篇文章的所有评论;

/reply: 所有评论;
/reply/<str: id>: 一条评论;


"""


def current_user():
    user_id = session.get('user_id', None)
    if user_id is None:
        return None
    # user_id = '599e598ec532091648c8079e'
    # print(user_id)
    u = User.query.filter_by(id=user_id)
    return u


@main.route('/boards')
def get_boards():
    boards = Board.query.all()
    return jsonify([board.to_json() for board in boards])


@main.route('/users')
def get_users():
    users = User.query.order_by(User.id.desc()).all()
    return jsonify([user.to_json() for user in users])


@main.route('/users/<int:id>')
def get_user():
    pass


@main.route('/posts')
def get_posts():
    param = request.args.get('board')
    if param == 'all':
        posts = Post.query.order_by(Post.timestamp.desc()).all()  # 倒序 desc()
    else:
        cur_board = Board.query.filter_by(name=param)
        posts = Post.query.filter_by(board_id=cur_board.id).order_by(Post.timestamp.desc()).all()
    return jsonify([post.to_json() for post in posts])


@main.route('/post/<int:id>')
def get_post():
    param = request.args.get('board')
    if param == 'all':
        posts = Post.query.all()
        return jsonify(posts)
    pass


@main.route('/register', methods=['POST'])
def register():
    req_json = request.json
    print('req_json:', req_json)  # dict
    user = User.register(req_json)
    return jsonify(user.to_json())


# '/login' 由 flask_jwt 定义


@main.route('/logout')
def logout():
    pass












