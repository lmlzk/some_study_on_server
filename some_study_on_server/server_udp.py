import socket

# 1. 创建套接字
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#2. bind绑定ip地址和端口，为元祖tuple类型
# ip如果不指明，表示本机的任何一个ip地址
server_addr = ("", 8089)
server_sock.bind(server_addr)
while True:
# recv方法接收发送过来的数据
# 返回值为接收到的数据，参数（这里为1024）表示本次收取数据的最大字节数
# receive_data = server_sock.recv(1024)
# recvfrom与recv方法类似，不同的是可以将发送数据的客户端的地址也返回
    receive_data, client_addr = server_sock.recvfrom(1024)
# 注意python3中收到的数据receive_data是bytes类型
# print(client_addr, ": ", receive_data)
# 将bytes数据转换为.字符串类型

    msg = receive_data.decode("utf-8")
# 将收到的数据显示输出
    print(client_addr, ": ", msg)
# 我们假定如果客户端发送了quit，我们就关闭服务端的套接字（即关闭服务端）
    if msg == "quit":
        server_sock.close()
        break