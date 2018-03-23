from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, jwt_required, current_identity, CONFIG_DEFAULTS
from config.config import database_uri
from datetime import timedelta
# current_identity: LocalProxy 本地代理, 返回req_ctx_stack.top中的identity
# 经过下面的函数定义, current_identity是个user实例

db = SQLAlchemy()
jwt = JWT()


def register_routes(app):
    """
    在 flask 中，模块化路由的功能由 蓝图（Blueprints）提供
    蓝图可以拥有自己的静态资源路径、模板路径
    用法如下
    注册蓝图
    有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀
    """
    # from routes.index import main as index_routes
    # from routes.post import main as post_routes
    # from routes.reply import main as reply_routes
    # from routes.board import main as board_routes
    # from routes.auth import main as auth_routes
    from api import main as api_routes  # 从这里导入models

    # app.register_blueprint(index_routes)
    app.register_blueprint(api_routes, url_prefix='/api')
    # app.register_blueprint(post_routes, url_prefix='/post')
    # app.register_blueprint(reply_routes, url_prefix='/reply')
    # app.register_blueprint(board_routes, url_prefix='/board')
    # app.register_blueprint(auth_routes)


def configure_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)


def configure_jwt(app):
    from models.user import User

    @jwt.authentication_handler
    def login(username, password):
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            return user

    # in flask_jwt:
    # _request_ctx_stack.top.current_identity = identity = _jwt.identity_callback(payload)
    @jwt.identity_handler
    def identity(payload):
        user_id = payload.get('identity', None)
        print('user_id: {}'.format(user_id))
        return User.query.filter_by(id=user_id).first()

    CONFIG_DEFAULTS['JWT_AUTH_URL_RULE'] = '/login'
    # CONFIG_DEFAULTS['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3000),  # 过期时间 3000s
    jwt.init_app(app)


def configured_app():
    app = Flask(__name__)
    configure_db(app)
    # 设置 secret_key 来使用 flask 自带的 session
    # 这个字符串随便你设置什么内容都可以
    app.secret_key = config.secret_key
    register_routes(app)
    configure_jwt(app)
    return app


if __name__ == '__main__':
    application = configured_app()
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=True,
        # host='0.0.0.0',
        host='127.0.0.1',
        port=2000,
    )
    application.run(**config)
