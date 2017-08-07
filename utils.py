import os.path
import time
import json


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('gua.log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def log2(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    # with open('gua.log.txt', 'a', encoding='utf-8') as f:
    print('**', dt, *args, **kwargs)


if __name__ == '__main__':
    format = '%Y-%m-%d %H:%M:%S'
    unix_time = int(time.time())  # 由float变成int
    value = time.localtime(unix_time)
    dt = time.strftime(format, value)
    print('untm: {}, \nvalue: {}, \ndt: {}'.format(unix_time, value, dt))