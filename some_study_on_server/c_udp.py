import socket

c_u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_add = ("127.0.0.1", 8089)
d = input("请求信息 : ")
c_u.sendto(d.encode("utf-8"), s_add)
ip = c_u.recv(1042)
print("收到信息："+ip.decode("utf-8"))
c_u.close()
