import threading
import json
from django.shortcuts import render
from django.http import HttpResponse
from spider.spiderPy.fetchByKeyWord import startSpider
from spider.spiderPy.fetchByKeyWord import testThread
import sys

# Create your views here.

"""
    drop第一次为1用于初始化数据库，之后设置为0
"""


def thread(type, themeArray, date, model_id, drop):
    for theme in themeArray:
        print('spider start')
        startSpider(type, theme, date, model_id, drop)
        #testThread()
        print('spider stop')
        sys.stdout.flush()
        drop = 0
    timer = threading.Timer(3600, thread, [
        type, themeArray, date, model_id, 1])
    timer.start()


def fetch(request):
    # type = request.GET.get('type')
    # POST
    req = json.loads(request.body)
    try:
        type = req['type']
        theme = req['theme']
        date = req['dayNum']
        model_id = req['warningModelId']
    except:
        return HttpResponse(-1)
    spider_thread = threading.Thread(target=thread,
                                     args=(type, theme, date, model_id, 1,))
    spider_thread.start()

    return HttpResponse(0)
