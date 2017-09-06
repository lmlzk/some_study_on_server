import socket
# 创建socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置socket可以重用地址
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
# 绑定本地信息
address = ('',8000)
server_sock.bind(address)
# 开启监听
server_sock.listen(128)
while True:
# 接收客户端的连接请求
    client_sock, client_addr = server_sock.accept()
    print("与客户端%s:%s建立了连接" % client_addr)
    while True:
    # 接收对方发送过来的数据，最大接收1024个字节
        recv_data = client_sock.recv(1024)
    # 如果接收的数据的⻓度为0，则意味着客户端关闭了链接
        if len(recv_data.decode()) >0:
            print("客户端说:%s" % recv_data.decode())
    # 发送一些数据到客户端
            msg = input("请输入回复的内容：")
            if msg == "\n":
                break
            else:
                client_sock.send(msg.encode())
        else:
            break
    print("客户端%s:%s已下线" % client_addr)
# 关闭客户端socket
    client_sock.close()
# 关闭服务器socket
server_sock.close()