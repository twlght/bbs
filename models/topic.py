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

    def user(self):
        from .user import User
        u = User.find_by_id(self.user_id)
        return u

    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms

