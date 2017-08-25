"""
注意，需要安装 pymongo 这个库
pip3 install pymongo


在你安装并开启 mongo 之后，就可以使用 pymongo 来链接使用 mongodb 了
"""

import pymongo


# 连接 mongo 数据库, 主机是本机, 端口是默认的端口
client = pymongo.MongoClient("mongodb://localhost:27017")

# 设置要使用的数据库
mongodb_name = 'mongo0818'
# 直接这样就使用数据库了，相当于一个字典
db = client[mongodb_name]
# 也可以这样用 db = client.web8


# 插入数据
# ===
# mongo 中的 document 相当于 sqlite 中的 table
# 不需要定义，直接使用
# 不限定每条数据的字段
# 直接插入新数据，数据以字典的形式提供
# 下面的例子中， user 是文档名（表名），不存在的文档会自动创建
# 每个数据有一个自动创建的字段 _id，可以认为是 mongo 自动创建的主键
import random


def insert():
    u = {
        'name': 'gua',
        'note': '瓜',
        # 放一个随机值来方便区分不同的数据以便下面的代码使用条件查询
        '随机值': random.randint(0, 3),
    }
    db.user.insert(u)
    print('insert a user')


def insert2():
    u = {
        'name': 'communication',
        'content': 'this is communication',
        'random num': random.randint(0,3),
        'date': '20170818',
    }
    db.topic.username.insert(u)
    # print('insert a user in topic')
    # 相当于 db['user'].insert


# 查找数据
# ===
# find 返回一个可迭代对象，使用 list 函数转为数组
def find():
    user_list = list(db.user.find())
    print('所有用户', user_list)


# find 可以传入参数来做条件查询
# 具体可以很复杂 我们这里只演示简单的
#
# 查询随机值为 1 的所有数据
def find1():
    query = {
        '随机值': 1,
    }
    print('random 1', list(db.user.find(query)))
    #
    # 查询 随机值 大于 1 的所有数据
    query = {
        '随机值': {
            '$gt': 1
        },
    }
    print('random > 1', list(db.user.find(query)))
    #
    # $or 查询
    query = {
        '$or': [
            {
               '随机值': 2,
            },
            {
                'name': 'GUA',
            }
        ]
    }
    us = list(db.user.find(query))
    print('or query', us)
#
#
# 此外还有 $lt $let $get $ne $or 等条件
#

# 部分查询, 相当于 select xx, yy from 表名 语句
#


def find_cond():
    query = {}
    field = {
        # 字段: 1 表示提取这个字段
        # 不传的 默认是 0 表示不提取
        'name': 1,
        # _id 默认是 1, 所以如果不想要 _id 必须主动干掉
        '_id': 0,
    }
    print('部分查询，只查询', list(db.user.find(query, field)))


# 更新数据
# ===
# 默认更新第一条查询到的数据
def update():
    query = {
        '随机值': 3,
    }
    form = {
        '$set': {
            'name': 'GW',
        }
    }
    # 可以有一个 options 参数来更新所有查询到的数据
    options = {
        'multi': True,
    }
    db.user.update(query, form, **options)
    # 上面的代码相当于下面这样
    # db.user.update(query, form, multi=True)


# 如果想要更新所有查询到的数据
# 需要加入下面的参数 {'multi': True}
# db.user.update(query, form, {'multi': True})


# 删除
# ===
# 删除和 find 是一样的
# db.user.remove({'id': 1})
def remove():
    query = {
        '随机值': 2
    }
    db.user.remove(query)


def main():
    insert2()
    # find()
    # find1()
    # find_cond()
    # update()
    remove()
    pass


if __name__ == '__main__':
    main()

"""
User.new(form)
User.all()
User.find_by(username='gua')

<SQL 必知必会>
<MySQL 必知必会>
"""