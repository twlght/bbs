import time
from pymongo import MongoClient  # pymongo v3.5
from bson.objectid import ObjectId

mongo_client = MongoClient()  # 默认localhost:27017


def timestamp():
    return int(time.time())


'''
pymongo中Collection的操作(Collection level operations):
bulk_write

insert_many
insert_one  替代insert()
replace_one  后两个替代save()

update_one
update_many  替代update()

delete_one
delete_many  替代remove()

find
find_one

find_one_and_delete
find_one_and_replace
find_one_and_update   这三个替代 find_and_modify 

count(Get the number of documents in this collection.)
各种index
drop(collection)
options(Get the options set on this collection.)
map_reduce
没有upsert方法, find方法的参数有upsert

find_one_and_update 与 update_one
find_one_and_update: 返回单个文档(BEFORE or AFTER)并update
update_one: update and return a instance of UpdateResult

API:
save
new
find
delete
'''


class Mongo(object):
    def __init__(self, form):
        if '_id' in form.keys():
            self._id = form.get('_id')  # ObjectId
            self.id = str(self._id)  # str -> _id
        self.type = form.get('type', self.__class__.__name__.lower())
        self.deleted = form.get('deleted', False)
        self.created_time = form.get('created_time', int(time.time()))
        self.updated_time = form.get('updated_time', int(time.time()))

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    @classmethod
    def insert_one(cls, *args, **kwargs):
        return mongo_client.db[cls.__name__].insert_one(*args, **kwargs)

    @classmethod
    def insert_many(cls, *args, **kwargs):
        return mongo_client.db[cls.__name__].insert_many(*args, **kwargs)

    @classmethod
    def update_one(cls, *args, **kwargs):
        return mongo_client.db[cls.__name__].update_one(*args, **kwargs)

    @classmethod
    def update_many(cls, *args, **kwargs):
        return mongo_client.db[cls.__name__].update_many(*args, **kwargs)

    @classmethod
    def replace_one(cls, *args, **kwargs):
        return mongo_client.db[cls.__name__].replace_one(*args, **kwargs)

    @classmethod
    def replace_many(cls, *args, **kwargs):
        return mongo_client.db[cls.__name__].replace_many(*args, **kwargs)

    @classmethod
    def find(cls, *args, **kwargs):
        collection = mongo_client.db[cls.__name__]
        # TODO 过滤掉被删除的元素
        if '_id' in kwargs.keys() and \
                not isinstance(kwargs['_id'], ObjectId):
                kwargs['_id'] = ObjectId(kwargs['_id'])
        bs = collection.find(kwargs)
        # bs 是 Cursor object, 对其迭代->call __next__() ->  \
        # -> 在__next__()中生成_Query instance, 发送查询数据, 返回dict类型
        # for b in bs:
        #     print(b)
        ms = [cls._new_with_bson(b) for b in bs]
        return ms

    @classmethod
    def new(cls, *args, **kwargs):
        return cls.new_and_save(*args, **kwargs)

    @classmethod
    def new_and_save(cls, form=None, **kwargs):
        if form is None:
            form = {}
        m = cls(form)
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        m.save()
        # cls.insert_one(m.__dict__)
        return m

    @classmethod
    def _new_with_bson(cls, bson):  # bson : dict
        # print(bson)
        if bson is None:
            bson = {}
        m = cls(bson)
        # setattr(m, '_id', bson['_id'])
        return m

    @classmethod
    def all(cls):
        return cls.find()

    @classmethod
    def find_all(cls, **kwargs):
        return cls.find(**kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        collection = mongo_client.db[cls.__name__]
        # TODO
        if '_id' in kwargs.keys() and \
                not isinstance(kwargs['_id'], ObjectId):
                kwargs['_id'] = ObjectId(kwargs['_id'])
        document = collection.find_one(kwargs)
        # document['_id'] -> ObjectId
        # print(document)
        if document is None:
            return None
        else:
            m = cls._new_with_bson(document)
            return m

    @classmethod
    def find_by_id(cls, id):
        return cls.find_one(_id=id)

    @classmethod
    def find_one_and_delete(cls, *args, **kwargs):
        collection = mongo_client.db[cls.__name__]
        # TODO 过滤掉被删除的元素
        document = collection.find_one_and_delete(*args, **kwargs)
        return document

    @classmethod
    def find_one_and_update(cls, *args, **kwargs):
        collection = mongo_client.db[cls.__name__]
        # TODO 过滤掉被删除的元素
        document = collection.find_one_and_update(*args, **kwargs)
        return document

    @classmethod
    def find_one_and_replace(cls, *args, **kwargs):
        collection = mongo_client.db[cls.__name__]
        # TODO 过滤掉被删除的元素
        document = collection.find_one_and_replace(*args, **kwargs)
        return document

    @classmethod  # update and insert
    def upsert(cls, filter_form, update_form, **kwargs):
        # collection = mongo_client.db[cls.__name__]
        ms = cls.find_one_and_update(filter_form, update_form, **kwargs)
        if ms is None:
            filter_form.update(**update_form)  # dict.update
            ms = cls.new_and_save(filter_form)
            # ms.update(update_form, hard=hard)
        return ms

    @classmethod
    def delete(cls, **filter_form):
        # todo!!!
        ms = cls.find_one_and_update(filter_form, {'deleted': True})
        return ms

    @classmethod
    def real_delete(cls, **filter_form):
        # todo!!!
        ms = cls.find_one_and_delete(filter_form)
        return ms

    @classmethod
    def count(cls):
        # todo
        pass

    def update(self, **update_form):
        if hasattr(self, '_id'):
            return self.update_one({'_id': self._id}, update_form)
        else:
            raise KeyError  # TODO 找个合适的ERROR

    def save(self):
        # __init__出来还未储存的没有'_id"
        if hasattr(self, '_id'):
            id = self.__dict__.pop('id')
            self.replace_one({'_id': self._id}, self.__dict__)
            setattr(self, 'id', str(id))
        else:
            r = self.insert_one(self.__dict__)  # insert_one 参数是一个dict
            setattr(self, '_id', r.inserted_id)
            setattr(self, 'id', str(r.inserted_id))

            # insert_one or replace_one
            # return self.upsert(query_form=self.__dict__, update_form=None)

            # collection = mongo_client.db[self.__class__.__name__]
            # # # print(self.__dict__)  # 这时没有'_id'
            # collection.save(self.__dict__)  # 现在有了'_id'

    @staticmethod
    def localtime(tm):
        format = '%Y-%m-%d %H:%M:%S'
        value = time.localtime(tm)
        dt = time.strftime(format, value)
        return dt


def tst():
    d = {
        'id': 5,
    }
    if 'id' in d.keys():
        print('True')
    # r = Mongo(form)
    # print(r._id)
    # r.id = 1
    # r.save()
    # foo = Mongo.new(form)
    # Mongo.delete(id=5)
    # print(ms)
    # mongo_client.drop_database('data')  # delete database
    # ms = mongo_client.db['Mongo'].insert_one({'id': 5}, {'$set': {'deleted': False}})
    # Mongo.replace_one({'id': 1}, {'deleted': False})  # 第二个参数, 要整个document, 不然就用update
    # print(ms)

    pass


if __name__ == '__main__':
    tst()