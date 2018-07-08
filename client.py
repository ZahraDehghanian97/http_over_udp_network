import socket
import select


# function section
def reliable_send(message, ip):
    global received
    received = 2  # 0 just send    1 receive ok   2 time out/send
    callSend = 1
    fragment = 0
    if len(message) > 6500:
        callSend = int(len(message) / 6500) + 1
        fragment = 1  # 1 moreFragment    0 o.w
    for x in range(0, callSend):
        start = x * 6500
        end = (x + 1) * 6500
        if x == callSend:
            fragment = 0
        FragmentedMESSAGE = str(x) + '*' + str(fragment) + '*' + MESSAGE[start: end] + '*' + str(ip) + "*" + make_parity(message)
        print("send packet : " + FragmentedMESSAGE)
        if reliable_send_fragmented(FragmentedMESSAGE):
            print("send succsecfully packet : " + str(x))
            print("\n")
            x += 1
            received = 2
        else:
            print("can not send packet number : " + str(x))
            # parity  ip/port/split dns
            return False
    return True


def reliable_send_fragmented(message):
    counter = 0
    global received
    while counter < 15:
        if received == 0:
            result = receive_http()
        if received == 1:
            counter = 15
            return True
        if received == 2:
            send_http(message)
            counter += 1

    if counter == 15 and received == 2:
        print("proxy is not ready to answer")
        return False


def check_parity(message):
    # m[2] data - m[4] parity
    temp = str(message)
    m = temp[2:-1].split('*')
    p = 0
    for i in m[2]:
        p += ord(i)
    parity = bin(p)
    parity = parity.split('b')
    if m[4] == parity[1]:
        return True
    else:
        return False


def make_parity(message):
    parity = 0
    p = 0
    for i in message:
        p += ord(i)
    parity = bin(p)
    parity = parity.split('b')
    return parity[1]


def send_http(message):
    global received
    # print("send packet")
    # print("UDP target IP:", UDP_IP_s)
    # print("UDP target port:", UDP_PORT_s)
    # print("message:", message)
    sock_send.sendto(bytes(message, "utf-8"), (UDP_IP_s, UDP_PORT_s))
    received = 0


def receive_http():
    global received
    print("client waiting for answer ...")
    ready = select.select([sock_receive], [], [], 1)
    if ready[0]:
        receive_data, addr = sock_receive.recvfrom(1024)  # buffer size is 1024 bytes
        # print("client receive message ")
        if check_parity(receive_data):
            received = 1
            assert isinstance(receive_data, object)
            show_result(receive_data)
            return receive_data
        else:
            received = 2
            print("parity error")
            return 0

    else:
        received = 2
        print("time out ")
        return 0


def show_result(message):
    assert isinstance(message, object)
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
received = 2  # 0 just send    1 receive ok   2 time out/send
# MESSAGE = "GET / HTTP/1.0\r\n\r\n"
DES_IP = input("enter destionation IP : ")
MESSAGE = input("enter your http message : ")
reliable_send(MESSAGE, DES_IP)

# parity  ip/port/split dns

# dns type setting numberOfPacke * moreFragment * message * IPDestination * parity
