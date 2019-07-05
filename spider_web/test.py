import threading
import datetime
import re
import sys
import time


def thread(self, input):
    for i in range(10):
        print('hello+'+str(input))
        time.sleep(2)
        if i == 4:
            print('stop')
            self.stop()


def change(input):
    input = 0

# for i in range(3):
#    th = threading.Thread(target=thread, args=(i,))
#    th.start()
#input = 11
# change(input)
# print(input)


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True


    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False


    def run(self):
        print('hello')
        self.stop()
        print('hello')
        #thread(self, input)

#st = StoppableThread()
#st.start()
def judgeTime(post_date, days_ago):
    constraint_date = (datetime.datetime.now() +
                       datetime.timedelta(days=-days_ago)).strftime("%Y-%m-%d")
    m_constraint = re.match(r'(\d{4})-(\d{2})-(\d{2})', constraint_date)
    constraint_year = m_constraint.group(1)
    constraint_month = m_constraint.group(2)
    constraint_day = m_constraint.group(3)
    try:
        m_date = re.match(r'(\d{4})-(\d{2})-(\d{2})', post_date)
        if int(constraint_year) < int(m_date.group(1)):
            return True
        if int(constraint_year) == int(m_date.group(1)):
            if int(constraint_month) < int(m_date.group(2)):
                return True
            if int(constraint_month) == int(m_date.group(2)):
                if int(constraint_day) < int(m_date.group(3)):
                    return True
                if int(constraint_day) == int(m_date.group(3)):
                    return True
    except:
        print('process time error')
    return False
print(judgeTime('2019-06-01',10))
