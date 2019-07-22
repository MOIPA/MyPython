# ThreadLocal可以用于处理局部变量共享问题
# 比如A函数传递参数a给B函数，B再传给C函数，非常麻烦。但是如果a参数改为全局变量需要加锁使用。所以出现了ThreadLocal
import threading
local_school = threading.local()


class Student(object):
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def __str__(self):
        return 'name %s age %s' % (self.__name, self.__age)


def process_student():
    print('hello % s(in % s)' %
          (local_school.student, threading.current_thread().name))


def process_thread(name, age):
    local_school.student = Student(name, age)
    # 这里就不需要传递参数了，子函数直接从local_school里面就可以通过线程名获取
    process_student()


t1 = threading.Thread(target=process_thread,
                      args=('alice', 11,), name='Thread-A')
t2 = threading.Thread(target=process_thread,
                      args=('Bob', 18,), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
