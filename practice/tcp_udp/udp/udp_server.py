import socket


if __name__ == '__main__':
    # sock_DGRAM 为udp协议
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind(('127.0.0.1', 23333))
    print('udp server binded')
    # 不需要listen，只需要读取数据，不用建立链接
    while True:
        data, addr = s.recvfrom(1024)
        print('received from %s:%s' % addr)
        s.sendto(('hello, %s!' % data).encode('utf-8'), addr)
