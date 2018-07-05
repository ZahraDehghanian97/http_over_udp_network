import socket
import select


# function section
def reliable_send(message):
    counter = 0
    global received
    while counter < 15:
        if received == 0:
            result = receive()
            print(received)
        if received == 1:
            if parity(message):
                counter = 15
                show_result(result)
            else:
                received = 2
        if received == 2:
            send(MESSAGE)
            counter += 1

    if counter == 15 and received == 2:
        print("proxy is not ready to answer")


def parity(message):
    # must be implement
    return True


def send(message):
    global received
    print("send packet")
    print("UDP target IP:", UDP_IP_s)
    print("UDP target port:", UDP_PORT_s)
    print("message:", message)
    sock_send.sendto(bytes(message, "utf-8"), (UDP_IP_s, UDP_PORT_s))
    received = 0


def receive():
    global received
    print("client waiting for answer ...")
    ready = select.select([sock_receive], [], [], 1)
    if ready[0]:
        receive_data, addr = sock_receive.recvfrom(1024)  # buffer size is 1024 bytes
        print("client receive message ")
        received = 1
        assert isinstance(receive_data, object)
        return receive_data
    else:
        received = 2
        print("time out ")
        return


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
sock_receive.setblocking(0)

# code section
received = 0  # 0 just send    1 receive ok   2 time out
MESSAGE = "GET / HTTP/1.0\r\n\r\n"
