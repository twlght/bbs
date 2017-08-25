# import time
from . import Mongo as Model


class Board(Model):
    def __init__(self, form):
        super().__init__(form)
        # self.id = None
        self.board_name = form.get('board_name', 'NoName')
        # self.ct = int(time.time())

    def topics(self):
        from models.topic import Topic
        ts = Topic.find_all(board_id=self.id)  # str
