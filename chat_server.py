import os

from socket import *

#  服务器地址
ADDR = ('0.0.0.0', 8888)

#  user_info containner
#  used for checking NAME is REAPT or NOT
user = {}


#   login
def do_login(s, name, addr):
    if name in user or "管理员" in name:
        s.sendto('USED_NAME'.encode(), addr)
        return
    s.sendto(b"OK", addr)
    #  prompt existent users another new member getting in
    msg = '\n %s 进入聊天室.' % name
    for i in user:
        s.sendto(msg.encode(), user[i])
    #  save USER_INFO
    user[name] = addr


#  chating function
def do_chat(s, name, text):
    msg = "\n%s : %s" % (name, text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])


# quit chat_room
def do_quit(s, name):
    msg = "\n%s exited" % name
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])
        else:
            s.sendto(b'EXIT', user[i])
    #  delete user
    del user[name]


#  循环接收请求
def do_request(s):
    while True:
        msg, addr = s.recvfrom(1024)
        # confirm request type

        msg = msg.decode().split(' ')
        if msg[0] == 'L':
            do_login(s, msg[1], addr)
        elif msg[0] == "C":
            text = ' '.join(msg[2:])
            do_chat(s, msg[1], text)
        elif msg[0] == 'Q':
            #  处理服务端重启后 客户端没有退出的情况
            #  可以把user设置为txt解决这个问题
            if msg[1] not in user:
                s.sendto(b'EXIT', addr)
                continue
            do_quit(s, msg[1])


#  创建网络连接
def main():
    #  套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        while True:
            text = input('管理员消息:')
            msg = "C 管理员消息 " + text
            s.sendto(msg.encode(), ADDR)
            # do_chat(s, "管理员消息", text.encode())
    else:
        #  请求
        do_request(s)  # 处理客户端请求


if __name__ == '__main__':
    main()
