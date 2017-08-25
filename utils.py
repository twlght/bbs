import os.path
import time
import json
import logging
import sys


# def get_cur_info():
#     print(os.path.relpath(sys._getframe().f_code.co_filename), ) #当前文件名，可以通过__file__获得
#     print(sys._getframe(0).f_code.co_name)   #当前函数名
#     print(sys._getframe(1).f_code.co_name)
#     #调用该函数的函数的名字，如果没有被调用，则返回<module>，貌似call stack的栈低
#     print(sys._getframe().f_lineno) #当前行号


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
    # get_cur_info()


if __name__ == '__main__':
    # format = '%Y-%m-%d %H:%M:%S'
    # unix_time = int(time.time())  # 由float变成int
    # value = time.localtime(unix_time)
    # dt = time.strftime(format, value)
    # print('untm: {}, \nvalue: {}, \ndt: {}'.format(unix_time, value, dt))
    log2('!!!')