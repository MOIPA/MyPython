'''
创建Socket时，AF_INET指定使用IPv4协议，如果要用更先进的IPv6，就指定为AF_INET6。SOCK_STREAM指定使用面向流的TCP协议，这样，一个Socket对象就创建成功，但是还没有建立连接。

客户端要主动发起TCP连接，必须知道服务器的IP地址和端口号。新浪网站的IP地址可以用域名www.sina.com.cn自动转换到IP地址
'''
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立链接
s.connect(('www.baidu.com', 80))
# 发送数据请求
s.send(b'GET / HTTP/1.1\r\nHost: www.baidu.com\r\nConnection: close\r\n\r\n')
# 接受数据
buffer = []
while True:
    # 每次最多接受1k字节
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)
# 关闭链接
s.close()

# 查看数据
header, html_body = data.decode('utf-8').split('\r\n\r\n', 1)
print(html_body)
