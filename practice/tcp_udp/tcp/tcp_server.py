
'''
服务器段编程，需要打开端口随时监听链接
所以，服务器会打开固定端口（比如80）监听，每来一个客户端连接，就创建该Socket连接。由于服务器会有大量来自客户端的连接，所以，服务器要能够区分一个Socket连接是和哪个客户端绑定的。一个Socket依赖4项：服务器地址、服务器端口、客户端地址、客户端端口来唯一确定一个Socket。

但是服务器还需要同时响应多个客户端的请求，所以，每个连接都需要一个新的进程或者新的线程来处理，否则，服务器一次就只能服务一个客户端了。

我们来编写一个简单的服务器程序，它接收客户端连接，把客户端发过来的字符串加上Hello再发回去。
'''

import socket
import threading
import time


def proceed(sock, addr):
    print('connect from %s:%s' % addr)
    sock.send(b'welcome')
    while True:
        data = sock.recv(1024).decode('utf-8')
        time.sleep(1)
        if data == 'exit' or not data:
            break
        sock.send(('hello , %s!' % data).encode('utf-8'))
    sock.close()
    print('connection from %s:%s closed' % addr)


if __name__ == '__main__':
    # 创建socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定地址
    s.bind(('127.0.0.1', 23333))
    # 开始监听
    s.listen(5)
    print('waiting for connection')
    # 每个连接用一个线程处理
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=proceed, args=(sock, addr))
        t.start()
