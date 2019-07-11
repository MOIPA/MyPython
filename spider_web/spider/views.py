import threading
import sys
import json
from django.shortcuts import render
from django.http import HttpResponse
from spider.spiderPy.fetchByKeyWord import startSpider
from spider.spiderPy.fetchByKeyWord import testThread

# Create your views here.


class ThreadPool(object):
    _count = 0
    _pool = {}

    @property
    def pool(self):
        return ThreadPool._pool

    @pool.setter
    def pool(self, pool):
        ThreadPool._pool = pool

    @property
    def count(self):
        return ThreadPool._count

    @count.setter
    def count(self, count):
        ThreadPool._count = count


"""
    drop第一次为1用于初始化数据库，之后设置为0
"""


def thread(d_type, themeArray, date, model_id, drop):
    thread_pool = ThreadPool()
    for theme in themeArray:
        print('start')
        sys.stdout.flush()
        # store in pool
        thread_pool.pool[thread_pool.count] = True
        startSpider(d_type, theme, date, model_id, drop,
                    thread_pool.count, thread_pool)
        thread_pool.count += 1
        # testThread()
        print('stop')
        sys.stdout.flush()
        drop = 0
    timer = threading.Timer(3600, thread, [
        d_type, themeArray, date, model_id, 1])
    # add in pool
    thread_pool = ThreadPool()
    thread_pool.pool += [timer.name, timer]
    timer.start()


def fetch(request):
    # type = request.GET.get('type')
    # POST
    print('fetch')
    req = json.loads(request.body)
    try:
        d_type = req['type']
        theme = req['theme']
        date = req['dayNum']
        model_id = req['warningModelId']
    except:
        return HttpResponse(-1)
    spider_thread = threading.Thread(target=thread,
                                     args=(d_type, theme, date, model_id, 1,))
    spider_thread.start()

    return HttpResponse(0)


def getThreadInfo(request):
    thread_pool = ThreadPool()
    return HttpResponse(thread_pool.count)
