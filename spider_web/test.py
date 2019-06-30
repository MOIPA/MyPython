import threading
import sys
import time


def thread(input):
    for i in range(10):
        print('hello+'+str(input))
        time.sleep(2)

def change(input):
    input=0

#for i in range(3):
#    th = threading.Thread(target=thread, args=(i,))
#    th.start()
input = 11
change(input)
print(input)
