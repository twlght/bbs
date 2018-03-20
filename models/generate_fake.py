from config.config import database_uri
from flask import Flask, current_app
from app import db
from models.board import Board
from models.user import User
from models.post import Post
from models.comment import Comment


def main():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # 需要应用上下文
    app_ctx = app.app_context()
    app_ctx.push()
    # db.init_app(app)
    db.init_app(current_app)
    db.drop_all()

    db.create_all()
    # create_all之前要执行所有class(Board, User, Post) 然后生成空的table
    Board.generate_boards()
    print('board generated')
    User.generate_fake(10)
    print('user generated')
    Post.generate_fake(40)
    print('post generated')
    Comment.generate_fake(220)
    print('comment generated')
    bs = Board.query.all()
    us = User.query.all()
    ps = Post.query.all()
    cs = Comment.query.all()
    # for l in ls:
    #     db.session.delete(l)  # 一个一个删
    # db.session.commit()  # list
    for ls in [bs, us, ps, cs]:
        for l in ls:
            print(l)


if __name__ == '__main__':
    main()