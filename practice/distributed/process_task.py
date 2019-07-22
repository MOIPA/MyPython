# 处理进程，从网络获取任务，处理，写入结果队列
import time
import sys
import queue as Queue
from multiprocessing.managers import BaseManager

# 自定义manager


class QueueManager(BaseManager):
    pass


# 标识要从网络获取的queue
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

server_addr = '127.0.0.1'
print('connect to server %s...' % server_addr)
# 链接到服务器的配置
m = QueueManager(address=(server_addr, 5000), authkey=b'123') #记得加b否则无法处理
# 执行链接
m.connect()
# 链接到服务器后获取两个队列
task = m.get_task_queue()
result = m.get_result_queue()
# 读取任务且处理
for i in range(10):
    try:
        n = task.get(timeout=3)
        print('run task %d * %d' % (n, n))
        time.sleep(1)
        result.put('%d * %d = %d' % (n, n, n*n))
    except Queue.Empty:
        print('task queue is empty')
print('exit')
