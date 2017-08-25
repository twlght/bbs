import time
from models import Mongo as Model
from bson.objectid import ObjectId


class Reply(Model):
    def __init__(self, form):
        super().__init__(form)
        # self.id = None
        self.content = form.get('content', '')
        # self.ct = int(time.time())
        # self.ut = self.ct
        self.topic_id = form.get('topic_id', '')
        self.user_id = form.get('user_id', '')  # user_id是在cls.new()里加上的

    def user(self):
        from .user import User
        u = User.find_by_id(self.user_id)  # str
        return u
