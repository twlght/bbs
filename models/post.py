from flask import url_for
from app import db
from config.config import database_uri
import datetime
from flask_jwt import jwt_required, current_identity
from sqlalchemy.exc import IntegrityError


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
    comments = db.relationship('Comment', backref='post', lazy='dynamic')  # 给Comment一个post属性

    def to_json(self):
        json_post = {
            # 'url': url_for('api.get_post', id=self.id, _external=True),
            'url': '/post/{}'.format(self.id),
            'title': self.title,
            'body': self.body,
            'timestamp': self.timestamp.date().isoformat(),
            'author': self.author.username,
            # 'author_url': url_for('api.get_user', id=self.author_id, _external=True),
            'authorURL': '/user/{}'.format(self.author_id),
            'authorId': self.author_id,
            'views': self.views,
            'board': self.board.name,
            'board_id': self.board_id,
            'comments': [comment.to_json() for comment in self.comments],
        }
        return json_post

    @classmethod
    def generate_post(cls, form):
        post = Post(title=form['title'],
                    board_id=form['boardId'],
                    body=form['content'],
                    author_id=current_identity.id,
                    )
        db.session.add(post)
        try:
            db.session.commit()
            print('generated a post: {}, id: {}'.format(post, post.id))
        except IntegrityError:
            db.session.rollback()
        return post

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
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(11, 93)),
                     title=forgery_py.lorem_ipsum.title(randint(1, 6)),
                     timestamp=forgery_py.date.date(True),
                     views=randint(1, 1000),
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
    pass

if __name__ == '__main__':
    # main()
    pass
