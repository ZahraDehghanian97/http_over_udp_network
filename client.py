import socket
import select


# function section
def reliable_send(message):
    counter = 0
    global received
    while counter < 15:
        if received == 0:
            result = receive_http()
        if received == 1:
            if parity(message):
                counter = 15

                return True
            else:
                received = 2
        if received == 2:
            send_http(message)
            counter += 1

    if counter == 15 and received == 2:
        print("proxy is not ready to answer")
        return False


def parity(message):
    # must be implement
    return True


def send_http(message):
    global received
    print("send packet")
    print("UDP target IP:", UDP_IP_s)
    print("UDP target port:", UDP_PORT_s)
    print("message:", message)
    sock_send.sendto(bytes(message, "utf-8"), (UDP_IP_s, UDP_PORT_s))
    received = 0


def receive_http():
    global received
    print("client waiting for answer ...")
    ready = select.select([sock_receive], [], [], 1)
    if ready[0]:
        receive_data, addr = sock_receive.recvfrom(1024)  # buffer size is 1024 bytes
        print("client receive message ")
        received = 1
        assert isinstance(receive_data, object)
        show_result(receive_data)
        return receive_data
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
MESSAGE = "GET / HTTP/1.0\r\n\r\n"
if len(MESSAGE) > 3:
    callSend = int(len(MESSAGE) / 3) + 1
    fragment = 1  # 1 moreFragment    0 o.w
for x in range(0, callSend):
    start = x * 3
    end = (x + 1) * 3
    if x == callSend:
        fragment = 0
    FragmentedMESSAGE = str(x) + '*' + str(fragment) + '*' + MESSAGE[start: end]
    print(FragmentedMESSAGE)
    if reliable_send(FragmentedMESSAGE):
        print("send succsecfully packet : " + str(x))
        x += 1
        received = 2
    else:
        print("can not send packet number : " + str(x))
        # parity  ip/port/split dns

# dns type setting numberOfPacke * moreFragment * message * IPDestination * portDestination

