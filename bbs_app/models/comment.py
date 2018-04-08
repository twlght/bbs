import datetime

from app import db


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.date.today())
    # author 来自User
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # post 来自Post
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def to_json(self):
        json_comment = {
            # 'url': url_for('api.get_post', id=self.id, _external=True),
            # 'url': '/post/{}'.format(self.id),
            # 'title': self.title,
            'body': self.body,
            'timestamp': self.timestamp.date().isoformat(),
            'author': self.author.username,
            'profilePhoto': self.author.profile_photo,
            # 'author_url': url_for('api.get_user', id=self.author_id, _external=True),
            'authorURL': '/user/{}'.format(self.author_id),
            # 'authorId': self.author_id,
            # 'views': self.views,
            # 'board': self.board.name,
            # 'post_id': self.post_id
        }
        return json_comment

    @staticmethod
    def generate_fake(count=10):
        from sqlalchemy.exc import IntegrityError
        from application.models import User
        from application.models.post import Post
        # from models.board import Board
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.query.count()
        # board_count = Board.query.count()
        post_count = Post.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            # b = Board.query.offset(randint(0, board_count - 1)).first()
            p = Post.query.offset(randint(0, post_count - 1)).first()
            c = Comment(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                        timestamp=forgery_py.date.date(True),
                        author=u,
                        post=p,
                        )
            db.session.add(c)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<Comment: {}>'.format(self.body)
