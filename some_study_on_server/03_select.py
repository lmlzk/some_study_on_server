import queue
import socket
import select

PORT = 8080

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

address = ("", PORT)
listen_sock.bind(address)

listen_sock.listen(128)

# 在该列表中保存让select进行判断是否能接收数据的套接字
input_list = [listen_sock]
# 客户端地址字典
in_msg_list = {}
# 在该列表中保存让select进行判断是否能发送数据的套接字
output_list = []

# # 消息容器队列
# {
#     "client1_sock":queue(msg1, msg2),
#     "clietn2_sock":...
# }
message_queue = {}

while 1:
    # 将input_list 与 output_list交给select进行遍历监视
    # input_list 表示 要select判断是否能够接收数据
    # output_list 表示 要select判断是否能够发送数据
    # 返回的recv_sock_list 中保存了能够立即接收数据的socket
    # 返回的send_sock_list 中保存了能够立即发送数据的socket
    recv_sock_list, send_sock_list, exception_sock_list = select.select(input_list, output_list, [])

    # 遍历处理可以接收数据或者接收请求的套接字列表recv_sock_list
    for sock in recv_sock_list:
        # 如果是监听的socket
        if sock is listen_sock:
            # 接收客户端的连接请求
            client_sock, client_addr = sock.accept()
            # client_msg = sock_msg.accept()
            print("客户端%s进行了连接" % str(client_addr))
            # 将对接该客户端的socket添加到input_list的任务中，让select判断什么时候有数据出来
            input_list.append(client_sock)
            # 创建跟该客户端对应的队列，用于保存对应该客户端socket可能发送的数据
            message_queue[client_sock] = queue.Queue()
            # 保存对应客户端疔地址
            in_msg_list[client_sock] = client_addr
        else:
            # 与客户端对应的socket，接收数据
            # (data, ancdata, msg_flags, address).
            # recv_data = sock.recvmsg(1024)
            recv_data = sock.recv(1024)
            if recv_data:
                # print(recv_data)
                print("客户端%s传来数据%s" % (str(in_msg_list[sock]), recv_data.decode()))
                # print("客户端传来数据%s" % recv_data.decode())
                # 因为send操作默认会阻塞，所以现将socket放到监视的队列中(output_list),由select来监视什么时候能够发送数据
                output_list.append(sock)
                # 将要发送的数据先保存到message_queue中
                message_queue[sock].put(recv_data)
            else:
                # 客户端关闭连接
                # 清除掉与该客户端对应的消息容器
                # 1清除与该客户端对应的地址表
                print("客户端%s关闭了连接" % str(in_msg_list[sock]))
                del message_queue[sock]
                del in_msg_list[sock]
                # 从input_list中移除掉该关闭的socket
                input_list.remove(sock)
                # 如果在output_list中也存在该socket，则也将其移除
                if sock in output_list:
                    output_list.remove(sock)
                # 关闭服务端与客户端通信的套接字
                sock.close()

    # 遍历处理返回的可以发送数据的套接字列表
    for sock in send_sock_list:
        # 如果与套接字对应的消息队列中的数据不为空，取 消息数据
        if not message_queue[sock].empty():
            msg = message_queue[sock].get()
            # 像客户端发送数据
            # msg_my = input("返回给%s的信息：" % str(in_msg_list[sock]))
            # sock.send((msg.decode()+msg_my).encode())
            sock.send(msg)
            # sock.send((msg_my).encode())
        else:
            # 如果消息队列中的数据为空，则表示数据已经发送完成，将sock从需要监视的output_list移除
            output_list.remove(sock)
