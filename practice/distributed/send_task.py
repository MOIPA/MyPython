# 分布式处理：此文件为分发任务和获取结果进程,处理进程不在此
import random
import time
import queue as Queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support 

# 发送任务队列
task_queue = Queue.Queue()
# 接受结果队列
result_queue = Queue.Queue()

# 自定义Queuemanager


class QueueManager(BaseManager):
    pass


# 将任务队列和结果队列注册到网络，处理进程从网络获取处理，结果写入
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)

# 绑定至端口5000，设置口令 ‘123’,初始化QueueManager
manager = QueueManager(address=('', 5000), authkey=b'123') # 一定加b因为需要传入的是byte类型不是str类型

#freeze_support()
# 启动Queue至网络
manager.start()

# 从网络中访问就是从manager中访问，现在manager里面包含这两个queue，只要能链接到manager的都可以访问
# 请注意，当我们在一台机器上写多进程程序时，创建的Queue可以直接拿来用，但是，在分布式多进程环境下，添加任务到Queue不可以直接对原始的task_queue进行操作，那样就绕过了QueueManager的封装，必须通过manager.get_task_queue()获得的Queue接口添加。

task = manager.get_task_queue()
#不能直接用之前创建的本地queue，只能通过网络queue
result = manager.get_result_queue()
# 放任务进入队列
for i in range(10):
    n = random.randint(0, 1000)
    print('put task %d...' % n)
    task.put(n)

# 读取其他进程的处理结果
# 其他进程负责将所有数据做乘方,结果不停的读，延时10秒，超过说明有错误
print('try get results')
for i in range(10):
    r = result.get(timeout=10)
    print('Result: %s ' % r)

# 服务结束 关闭
manager.shutdown()
