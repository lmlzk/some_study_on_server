import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
d = input("输入信息：")
s.sendto(d.encode("utf-8"), ("<broadcast>", 8080))
ip = s.recvmsg(1042)
print("返回信息："+ip.decode("utf-8"))
# print("返回信息：%s"% ip[0])
s.close()
