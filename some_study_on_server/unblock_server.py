import socket
# 用来存储所有的新链接的客户端
client_list = []
def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = ('', 8000)
    server_sock.bind(address)
    server_sock.listen(128)
# 将套接字设置为非堵塞
# 设置为非堵塞后，如果accept时，恰巧没有客户端connect，那么accept会
#  产生一个异常，所以需要try来进行处理
    server_sock.setblocking(False)
    while True:
        try:
            client_info = server_sock.accept()
        except BlockingIOError:
            pass
        else:
            print("一个新的客户端到来%s：" % str(client_info))
# 将套接字设置为非堵塞
            client_info[0].setblocking(False)
            client_list.append(client_info)
# 用来存储需要删除的客户端信息
        need_del_client_info_list = []
        for client_socket, client_addr in client_list:
            try:
                recv_data = client_socket.recv(1024)
                if len(recv_data) > 0:
                    print('recv[%s]:%s' % (str(client_addr), recv_data.decode()))
                else:
                    print('[%s]客户端已经关闭' % str(client_addr))
                    client_socket.close()
                    need_del_client_info_list.append((client_socket, client_addr))
            except BlockingIOError:
                pass
        for client in need_del_client_info_list:
            client_list.remove(client)
if __name__ == '__main__':
    main()