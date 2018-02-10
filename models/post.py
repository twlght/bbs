from flask import url_for
from app import db
from config.config import database_uri
import datetime


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.date.today())
    # author 来自User
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    views = db.Column(db.Integer, default=0)
    # board 来自Board
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'title': self.title,
            'body': self.body,
            'timestamp': self.timestamp.date().isoformat(),
            'author': self.author.username,
            'author_url': url_for('api.get_user', id=self.author_id, _external=True),
            'views': self.views,
            'board': self.board.name,
            'board_id': self.board_id
        }
        return json_post

    @staticmethod
    def generate_fake(count=10):
        from sqlalchemy.exc import IntegrityError
        from models.user import User
        from models.board import Board
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.query.count()
        board_count = Board.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            b = Board.query.offset(randint(0, board_count - 1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     title=forgery_py.lorem_ipsum.title(randint(1, 6)),
                     timestamp=forgery_py.date.date(True),
                     views=randint(1, 100),
                     author=u,
                     board=b)
            db.session.add(p)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<Post: {}>'.format(self.title)


def main():
    from flask import Flask, current_app
    from models.board import Board
    from models.user import User
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
    User.generate_fake(10)
    Post.generate_fake(30)
    bs = Board.query.all()
    us = User.query.all()
    ps = Post.query.all()
    # for l in ls:
    #     db.session.delete(l)  # 一个一个删
    # db.session.commit()  # list
    for ls in [bs, us, ps]:
        for l in ls:
            print(l)


if __name__ == '__main__':
    # main()
    pass