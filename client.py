import socket
import select


# function section


def send_dns(message):
    global received
    print("send packet")
    print("DNS target IP:", TCP_IP)
    print("DNS target port:", TCP_PORT)
    print("DNS target name:", TCP_Target)
    print("message:", message)
    newmsg = bytes(DNS_type + "*" + TCP_IP + "*" + TCP_Target + "*" + MESSAGE, 'utf-8')
    s.connect((TCP_IP, TCP_PORT))
    s.send(newmsg)


def receive_dns():
    global received
    print("client waiting for answer ...")

    data = s.recv(BUFFER_SIZE)
    s.close()
    show_result_dns(data)


def show_result_dns(message):
    print("received message:", message)






TCP_IP = '127.0.0.1'
TCP_PORT = 5005
TCP_Target = 'aut.ac.ir'
DNS_type = 'Aname'
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_dns(MESSAGE)

receive_dns()
