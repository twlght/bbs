import time
from models import Mongo as Model
from bson.objectid import ObjectId


class Topic(Model):
    def __init__(self, form):
        super().__init__(form)
        # self.id = None
        self.views = form.get('views', 0)
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        # self.ct = int(time.time())
        # self.ut = self.ct
        self.user_id = form.get('user_id')  # str
        self.board_id = form.get('board_id')  # str

    @classmethod
    def get(cls, id):
        m = cls.find_by_id(id)
        m.views += 1
        m.save()
        return m

    def board(self):
        from models.board import Board
        b = Board.find_by_id(self.board_id)
        return b

    def user(self):
        from models.user import User
        u = User.find_by_id(self.user_id)
        return u

    def replies(self):
        from models.reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms

    @staticmethod
    def generate_fake(count):
        import forgery_py
        from random import seed, randint
        from models.board import Board
        from models.user import User
        seed()

        users = User.all()
        boards = Board.all()
        for i in range(count):
            form = dict(
                title=forgery_py.lorem_ipsum.sentence(),
                content=forgery_py.lorem_ipsum.sentences(randint(1, 10)),
                user_id=users[randint(0, len(users)-1)].id,
                board_id=boards[randint(0, len(boards)-1)].id,
            )
            t = Topic(form)
            t.save()


def tst():
    Topic.generate_fake(200)


if __name__ == '__main__':
    tst()
