from app import db, jwt
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import UserMixin
from flask import url_for, session


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    # password 不可读
    password_hashed = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False, index=True)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime, default=datetime.date.today())
    # posts 是个query, 不是查询之后的结果 可以用for循环迭代出来.
    posts = db.relationship('Post', backref='author', lazy='dynamic')  # 给Post一个author属性
    comments = db.relationship('Comment', backref='author', lazy='dynamic')  # 给Comment一个author属性

    # to_json(), 将实例转化为json, 实际上是先变成dict返回, 在路由函数中jsonify
    def to_json(self):
        json_user = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'location': self.location,
            'quote': self.about_me,
            'member_since': self.member_since.isoformat(),
            'posts': [post.to_json() for post in self.posts]
        }
        return json_user

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hashed = self.hash_password(password)

    @staticmethod
    def hash_password(password, salt='$!@><?>HUI&DWQa`'):
        import hashlib

        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def verify_password(self, password):
        if self.password_hashed == self.hash_password(password):
            return True
        else:
            return False

    @staticmethod
    def validate_form(form):
        return True

    @classmethod
    def register(cls, form):
        if cls.validate_form(form):
            user = User(username=form['username'],
                        email=form['email'],
                        password=form['password'])
            db.session.add(user)
            db.session.commit()
            print('register a user: {}'.format(user))
            return user

    @staticmethod
    def generate_fake(count=10):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            if i == 0:
                user = User(
                    username='admin',
                    email=forgery_py.internet.email_address(),
                    password='123',
                    is_admin=True,
                    location=forgery_py.address.city(),
                    about_me=forgery_py.lorem_ipsum.sentence(),
                    member_since=forgery_py.date.date(True))
            else:
                user = User(
                    username=forgery_py.internet.user_name(True),
                    email=forgery_py.internet.email_address(),
                    password='123',
                    is_admin=False,
                    location=forgery_py.address.city(),
                    about_me=forgery_py.lorem_ipsum.sentence(),
                    member_since=forgery_py.date.date(True))
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<User: {}>'.format(self.username)


def main():
    pass


if __name__ == '__main__':
    main()
