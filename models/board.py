import time
from . import Model


class Board(Model):
    def __init__(self):
        self.id = None
        self.board_name = ''
        self.ct = int(time.time())

    def topics(self):
        from models.topic import Topic
        ts = Topic.find_all(board_id=self.id)