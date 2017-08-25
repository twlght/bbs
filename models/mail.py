from models import Mongo as Model
import time
'''
'''


class Mail(Model):
    def __init__(self, form):
        super().__init__(form)
        # self.id = None
        self.content = form.get('content', '')
        self.title = form.get('title', '')
        # self.ct = int(time.time())
        self.read = False
        self.sender_id = -1  # todo sender id
        self.receiver_id = form.get('receiver_id', -1)

    def mark_read(self):
        self.read = True
        self.save()

    def set_sender_id(self, sender_id):
        self.sender_id = sender_id
        self.save()
