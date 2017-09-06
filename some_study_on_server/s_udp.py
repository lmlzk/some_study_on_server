import socket

s_u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_add = ("", 8000)
s_u.bind(s_add)
do = {"廖明黎.com" : "127.0.0.1"}
rece_data, c_u = s_u.recvfrom(1042)
msg = rece_data.decode("utf-8")
ip = do.get(msg, "你要找得人太帅！")
s_u.sendto(ip.encode("utf-8"), c_u)
print(msg)
s_u.close()
