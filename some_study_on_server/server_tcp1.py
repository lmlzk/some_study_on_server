import socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
address = ("", 8000)
server_sock.bind(address)
server_sock.listen(4)
while True:
    client_con_sock, client_addr = server_sock.accept()
    print("客户端%s:%s进行了连接!" % client_addr)
    while True:
        recv_data = client_con_sock.recv(1024)
        if len(recv_data) > 0:
            print("接收到的数据为：", recv_data.decode())
            # client_con_sock.send("thank you!\n".encode())
            client_con_sock.send((recv_data.decode()+"lml").encode())
        else:
            break
    print("客户端%s:%s已下线" % client_addr)
    client_con_sock.close()
server_sock.close()