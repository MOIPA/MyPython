import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',23333))
print(s.recv(1024))
for data in ['tr','tzq']:
    s.send(data.encode('utf-8'))
    print(s.recv(1024))

s.send(b'exit')
s.close()
