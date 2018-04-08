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
    pass


if __name__ == '__main__':
    main()
