'''
Python的标准库提供了两个模块：thread和threading，thread是低级模块，threading是高级模块，对thread进行了封装。绝大多数情况下，我们只需要使用threading这个高级模块。

启动一个线程就是把一个函数传入并创建Thread实例，然后调用start()开始执行：
'''
import time
import threading


def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n+1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended' % threading.current_thread().name)


def start_loop():
    print('thread %s is running...' % threading.current_thread().name)
    t = threading.Thread(target=loop, name='LoopThread')
    t.start()
    t.join()
    print('thread %s ended' % threading.current_thread().name)


# start_loop()

# 以上只是一个简单的实例，线程和进程最大的不同是，线程的所有变量都是可以共享被修改的，容易导致脏数据
# 所以使用锁lock

import random
balance = 0
lock = threading.Lock()


def change_money(n):
    global balance
    print('thread % s is running before change: % s'% (threading.current_thread().name, balance))
    balance += n
    time.sleep(1)
    balance -= n


def run_change(n):
    for i in range(10):
        # 这里需要加锁
        time.sleep(random.random())
        lock.acquire()
        try:
            change_money(n)
        finally:
            # 一定要保证释放，否则等待线程死锁
            lock.release()
            pass


t1 = threading.Thread(target=run_change, args=(5,))
t2 = threading.Thread(target=run_change, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print('the balance result is :%s' % balance)
