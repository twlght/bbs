from models import Mongo as Model
import os


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    def __init__(self, form):
        super().__init__(form)
        # self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.filename = form.get('filename', 'my_pc.jpg')

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib

        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_one(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User(form)
        user = User.find_one(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None

    def topics(self):
        from models.topic import Topic
        ts = Topic.find_all(user_id=self.id)
        return ts

    @staticmethod
    def generate_fake(count):
        import forgery_py
        from random import randint
        img_list = os.listdir('../users_img')
        for i in range(count):
            form = dict(
                username=forgery_py.internet.user_name(False),
                password='123',
            )
            u = User(form)
            u.filename = img_list[randint(0, len(img_list)-1)]
            u.password = u.salted_password(u.password)
            u.save()


def tst():
    # print(os.listdir('../users_img'))
    User.generate_fake(10)
if __name__ == '__main__':
    tst()