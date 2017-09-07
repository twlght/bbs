from flask import session

from models.user import User
from bson.objectid import ObjectId


def current_user():
    user_id = session.get('user_id', None)
    if user_id is None:
        return None
    # user_id = '599e598ec532091648c8079e'
    # print(user_id)
    u = User.find_by_id(user_id)  # str
    return u


if __name__ == '__main__':
    # class A():
    #     def __init__(self):
    #         self.s1 = 'str'
    #         self.s2 = 'repr'
    #
    #     def __str__(self):
    #         return self.s1
    #
    #     def __repr__(self):
    #         return self.s2
    # uu = current_user()
    # print(uu)
    # a = A()
    # print(a)
    # s3 = '{}'.format(a)
    # print(s3)
    pass