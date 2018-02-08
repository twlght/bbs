from app import db
from flask import Flask, current_app, url_for
from flask_sqlalchemy import SQLAlchemy


class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    posts = db.relationship('Post', backref='board', lazy='dynamic')

    def to_json(self):
        json_board = {
            'id': self.id,
            'name': self.name,
        }
        return json_board

    @staticmethod
    def generate_boards():
        from sqlalchemy.exc import IntegrityError
        boards = ['python', 'linux', 'vue', 'mongodb', 'nginx']
        for b in boards:
            board = Board(name=b)
            db.session.add(board)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<board: {}>'.format(self.name)


def main():
    from models.post import Post
    from models.user import User
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://postgres:root@127.0.0.1:5432/bbsdb'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app_ctx = app.app_context()  # 需要应用上下文
    app_ctx.push()
    # db.init_app(app)
    db.init_app(current_app)
    # db.create_all()
    # create_all之前要执行所有class(Board, User, Post) 然后生成空的table
    # 之后就不用了
    Board.generate_boards()
    bs = Board.query.all()  # list
    print(bs)


if __name__ == '__main__':
    main()
