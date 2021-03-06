from flask import (
    request,
    Blueprint,
    jsonify,
)
from flask_jwt import jwt_required, current_identity
from utils import log
from models.user import User

main = Blueprint('auth', __name__)


@main.route('/register', methods=['POST'])
def register():
    req_json = request.json
    log('req_json:', req_json)  # dict
    user = User.register(req_json)
    return jsonify(user.to_json())


@main.route('/token_login')
@jwt_required()
def get_loggedin_user():
    log(jsonify(current_identity.to_json()))
    return jsonify(current_identity.to_json())
# '/login' 由 flask_jwt 定义


# 由前端直接删除token, 不用向后端发request 也就是说这个现在没用
@main.route('/logout')
def logout():
    pass
