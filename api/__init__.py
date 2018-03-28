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
from flask_jwt import jwt_required, current_identity
from models.user import User
from models.post import Post
from models.board import Board
from models.comment import Comment


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


@main.route('/boards')
def get_boards():
    boards = Board.query.all()
    return jsonify([board.to_json() for board in boards])


@main.route('/users')
def get_users():
    users = User.query.order_by(User.id.desc()).all()
    return jsonify([user.to_json() for user in users])


@main.route('/user/<params>')
def get_user_by_id(params):
    print('params: {}'.format(params))
    print('type: {}'.format(type(params)))
    if params.isdigit():
        id = int(params)
        user = User.query.filter_by(id=id).first()
        return jsonify(user.to_json())
    else:
        username = params
        user = User.query.filter_by(username=username).first()
        return jsonify(user.to_json())


# ?board=xxx or ?user_id=xxx
@main.route('/posts', methods=['GET'])
def get_posts():
    board_name = request.args.get('board', None)
    user_id = request.args.get('user_id', None)
    if board_name:
        if board_name == 'all':
            posts = Post.query.order_by(Post.timestamp.desc()).all()  # 倒序 desc()
        else:
            cur_board = Board.query.filter_by(name=board_name).first()
            # print(cur_board)
            # 前端axios查询board的方式由board.id改为board.name, 后端做相应适配修改
            posts = Post.query.filter_by(board_id=cur_board.id).order_by(Post.timestamp.desc()).all()
        return jsonify([post.to_json() for post in posts])
    if user_id:
        posts = Post.query.filter_by(author_id=int(user_id)).order_by(Post.timestamp.desc()).all()
        return jsonify([post.to_json() for post in posts])


@main.route('/posts', methods=['POST'])
@jwt_required()
def post_post():
    print('request headers: {}'.format(request.headers))
    # current_user = current_identity
    print('current_identity: ', current_identity)
    req_json = request.json
    print('req_json:', req_json)  # dict
    post = Post.generate_post(req_json)
    return jsonify(post.to_json())


@main.route('/post/<int:id>')
def get_post(id):
    # id = request.args.get('id')
    post = Post.query.filter_by(id=int(id)).first()
    return jsonify(post.to_json())


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












