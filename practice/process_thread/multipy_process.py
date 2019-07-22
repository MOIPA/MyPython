# linux 下
from multiprocessing import Process, Queue
import random
import time
from multiprocessing import Pool
from multiprocessing import Process
import os


def linux_only_process():
    print('os now is %s' % os.getpid())
    # fork是linux和unix里面的专用函数，windows下不可用。且会返回两次，父进程返回0，执行以下函数。但是同时子进程也也在跑，返回自己的pid。
    # 个人感觉fork不如用库，fork的子进程会自动执行fork点后的所有代码，不方便分离子和父代码
    pid = os.fork()
    if pid == 0:
        print('child process is %s and parent process is %s' %
              (os.getpid(), os.getppid()))
    else:
        print('parent process %s created a child process %s' %
              (os.getpid(), pid))

# windows 下

# 子进程要执行的代码


def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))


def multiprocessingTest():
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Process will start.')
    p.start()
    p.join()  # join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步。
    print('Process end.')


multiprocessingTest()

print("*****************************")

# 线程池


def long_time_task(name):
    print('run task %s:%s' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random()*3)
    end = time.time()
    print('task %s run %0.2f seconds' % (name, (end-start)))


'''
对Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process了。

请注意输出的结果，task 0，1，2，3是立刻执行的，而task 4要等待前面某个task完成后才执行，这是因为Pool的默认大小在我的电脑上是4，因此，最多同时执行4个进程。这是Pool有意设计的限制，并不是操作系统的限制。如果改成：

p = Pool(5)
就可以同时跑5个进程。
'''


def pool_test():
    print('parent process %s' % os.getpid())
    p = Pool(3)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('waiting for all subprocesses done...')
    p.close()
    p.join()
    print('done')


# pool_test()
# print('*****************************')

# 进程通信  这里只看了queue没有pipe 也没有共享变量，需要的日后自行google
'''
Process之间肯定是需要通信的，操作系统提供了很多机制来实现进程间的通信。Python的multiprocessing模块包装了底层的机制，提供了Queue、Pipes等多种方式来交换数据。

我们以Queue为例，在父进程中创建两个子进程，一个往Queue里写数据，一个从Queue里读数据：
'''

# 写数据


def write(q):
    for value in ['a', 'b', 'c', 'd']:
        print('Put value %s' % value)
        q.put(value)
        time.sleep(random.random())


def read(q):
    while True:
        value = q.get(True)
        print('Get value %s' % value)


def communicate_test():
    # 创建queue 传递给子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动
    pw.start()
    pr.start()
    # 等待写结束
    pw.join()
    # pr是不停读取的死循环，直接杀死
    pr.terminate()


communicate_test()
