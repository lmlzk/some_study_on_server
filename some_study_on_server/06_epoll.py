import socket
import select
import queue

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 8080))
s.listen(128)

# 创建一个epoll对象（或者理解为一个epoll容器）
epoll = select.epoll()

# 向epoll中添加需要epoll进行监视管理的socket（通过socket文件编号--fileno()的返回值--进行注册）
# EPOLLIN表示要进行input监控，即监视什么时候能够执行recv或者accept操作
# EPOLLET表示边缘触发，即对于调用者的提醒仅提示一次
epoll.register(s.fileno(), select.EPOLLIN | select.EPOLLET)

# 用来保存文件编号与socket对应的关系
client_socks = {}
# 用来保存文件编号与客户端地址的对应关系
client_addrs = {}
# 用来保存要发送给客户端的消息数据
msg_queue = {}

while 1:
    # 询问epoll有无可以操作的socket，返回的epoll_list中包含可以进行处理的socket对应的文件编号
    epoll_list = epoll.poll()

    # 遍历能够处理的socket文件编号列表，依次进行处理
    # fd表示文件的编号
    # events表示是可以进行读取recv/accept操作还是可以进行写send操作
    for fd, events in epoll_list:
        # 如果是监听的socket文件
        if fd == s.fileno():
            # 接收客户端的请求
            conn, addr = s.accept()
            # 将连接的客户端的socket与地址保存
            client_socks[conn.fileno()] = conn
            client_addrs[conn.fileno()] = addr
            # 创建对应 该客户端的发送消息的队列
            msg_queue[conn.fileno()] = queue.Queue()
            print("%s已连接" % str(addr))
            # 将新的客户端的socket添加到epoll中进行监视管理
            epoll.register(conn.fileno(), select.EPOLLIN | select.EPOLLET)
        # 如果是可以进行读取数据accept/recv的套接字
        elif events == select.EPOLLIN:
            recv_data = client_socks[fd].recv(1024)
            if recv_data:
                print("%s传来数据%s" % (str(client_addrs[fd]), recv_data.decode()))
                # 将要发送给客户端的数据放到消息队列中
                msg_queue[fd].put(recv_data)
                # 将这个与客户端进行通信的socket在epoll中的监视行为改为监视可否发送数据
                epoll.modify(fd, select.EPOLLOUT | select.EPOLLET)
            else:
                # 客户端关闭了连接
                print("%s已关闭" % str(client_addrs[fd]))
                # 将socket从epoll中删除
                epoll.unregister(fd)
                # 删除与该socket对应的消息队列
                del msg_queue[fd]
                # 关闭该socket
                client_socks[fd].close()
                # 删除socket在cliet_socks和client_addrs中保存的数据
                del client_socks[fd]
                del client_addrs[fd]
        # 如果是可以进行发送数据send的套接字
        elif events == select.EPOLLOUT:
            # 消息队列中不为空，就取出数据发送
            while True:
                if not msg_queue[fd].empty():
                    msg = msg_queue[fd].get()
                    client_socks[fd].send(msg)
            # 没有消息数据了，就将对该socket的监视行为改为监视是否有数据从客户端发送过来
                else:
                    epoll.modify(fd, select.EPOLLIN | select.EPOLLET)
                    break
