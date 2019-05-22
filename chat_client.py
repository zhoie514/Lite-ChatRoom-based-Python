from socket import *
import os
import sys


#  server address
ADDR = ('176.221.19.5', 8888)


# send msg loop
def send_msg(s, name):
    while True:
        try:
            text = input('Speak:')
        #  keyboard quit
        except KeyboardInterrupt:
            text = "quit"

        #  quit chat_room
        if text == "quit":
            msg = "Q " + name
            s.sendto(msg.encode(), ADDR)
            sys.exit("exit Chatting Room ...")

        msg = "C %s %s" % (name, text)
        s.sendto(msg.encode(), ADDR)


#  recieve msg loop
def recv_msg(s):
    while True:
        data, addr  = s.recvfrom(1024)
        #  recieved"EXIT" Prompting quit chatting room
        if data.decode() == 'EXIT':
            sys.exit()
        print(data.decode() + '\nSpeak:',end='')



#  build socket
def main():
    client = socket(AF_INET, SOCK_DGRAM)
    while True:
        #  set name and confirm
        name = input('Set Your Name: ')
        msg = 'L ' + name
        client.sendto(msg.encode(), ADDR)
        #  waiting responce(s)
        confirm_info, addr = client.recvfrom(1024)
        if confirm_info.decode() == "OK":
            print('Getting ChatRoom Sucessfully...')
            break
        else:
            print(confirm_info.decode())

    #  creat new process
    pid = os.fork()
    if pid < 0:
        sys.exit("Error")
    elif pid == 0:
        send_msg(client, name)
    else:
        recv_msg(client)


if __name__ == '__main__':
    main()
