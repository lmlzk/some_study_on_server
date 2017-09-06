import socket
# 创建客户端socket用以跟服务器连接通信
# tcp协议对应为SOCK_STREAM
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect方法用来连接服务器
# server_addr = ("192.168.71.99", 8080)
server_addr = ("127.0.0.1", 9000)
client_sock.connect(server_addr)
# 提示用户输入要发送的数据
msg = input("请输入要发送的内容2：")
# send()方法想服务器发送数据
client_sock.send(msg.encode())
print("已发送")
# recv()接收对方发送过来的数据，最大接收1024个字节
recv_data = client_sock.recv(1024)
print("收到了服务器的回应信息：%s" % recv_data.decode())
# 关闭客户端套接字
client_sock.close()
