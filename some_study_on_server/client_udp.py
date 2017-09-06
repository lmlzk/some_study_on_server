import socket
# 1. 创建套接字
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 服务器地址
server_addr = ('127.0.0.1', 8089)
data = input("请输入要发送的内容：")
# 只要用户输入的数据不为空，就向服务器端发送
while data:
# 2. 使用sendto方法向服务器发送数据
# sendto(bytes类型要发送的数据，对方的地址)
    client_sock.sendto(data.encode("utf-8"), server_addr)
    data = input("请输入要发送的内容：")
# 当用户输入的数据为空（"")时, 关闭客户端套接字
client_sock.close()