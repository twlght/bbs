from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    jsonify,
)
from models.user import User


main = Blueprint('auth', __name__)


@main.route('/register', methods=['POST'])
def register():
    req_json = request.json
    print('req_json:', req_json)  # dict
    user = User.register(req_json)
    return jsonify(user.to_json())


# '/login' 由 flask_jwt 定义


# 由前端直接删除token, 不用向后端发request
@main.route('/logout')
def logout():
    pass
