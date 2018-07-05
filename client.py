import socket


# function section
def send(message):
    print("UDP target IP:", UDP_IP_s)
    print("UDP target port:", UDP_PORT_s)
    print("message:", message)
    sock_send.sendto(bytes(message, "utf-8"), (UDP_IP_s, UDP_PORT_s))
    received = 0


def receive():
    print("client waiting for answer ...")
    while (True):
        try:
            receive_data, addr = sock_receive.recvfrom(1024)  # buffer size is 1024 bytes
            print("client receive message ")
            received = 1
            assert isinstance(receive_data, object)
            return receive_data
            break

        except socket.timeout:
            received = 2
            print("time out :( ")
            break


def show_result(message):
    print("received message:", message)


# send part initiation
UDP_IP_s = "127.0.0.1"  # "185.211.88.22"
UDP_PORT_s = 5005
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

# receive part initiation
UDP_IP_r = "127.0.0.1"  # "185.211.88.22"
UDP_PORT_r = 5006
sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock_receive.bind((UDP_IP_r, UDP_PORT_r))
sock_receive.settimeout(0.00001)

# code section
received = 0  # 0 just send    1 receive ok   2 time out
MESSAGE = "GET / HTTP/1.0\r\n\r\n"

counter = 0
while counter < 15:
    if received != 0:
        send(MESSAGE)
    else:
        result = receive()
    if received == 1:
        counter = 15
        show_result(result)
    elif received == 2:
        counter += 1

if counter == 15 and received == 2:
    print("proxy is not ready to answer")
