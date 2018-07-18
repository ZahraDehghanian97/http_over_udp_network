import socket
import socket
import select
import codecs


# function section

def reliable_send(message, ip):
    global received, sock_send, sock_receive
    sock_receive.bind((UDP_IP_r_proxy, UDP_PORT_r_proxy))
    sock_receive.setblocking(0)
    sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    received = 2  # 0 just send    1 receive ok   2 time out/send
    callSend = 1
    fragment = 0
    if len(message) > 1024:
        callSend = int(len(message) / 1024) + 1
        fragment = 1  # 1 moreFragment    0 o.w
    for x in range(0, callSend):
        start = x * 1024
        end = (x + 1) * 1024
        print(callSend)
        if x == callSend - 1:
            fragment = 0
        FragmentedMESSAGE = str(x) + '*@--' + str(fragment) + '*@--' + MESSAGE[start: end] + '*@--' + str(
            ip) + "*@--" + make_parity(MESSAGE[start: end])
        print("send packet : " + FragmentedMESSAGE)
        if reliable_send_fragmented(FragmentedMESSAGE):
            print("send successfully packet number " + str(x))
            print("\n")
            x += 1
            received = 2
        else:
            print("can not send packet number " + str(x))
            # parity  ip/port/split dns
            return False
    sock_send.close()
    sock_receive.close()
    return True


def reliable_send_fragmented(message):
    counter = 0
    global received
    while counter < 15:
        if received == 0:
            result = receive_http_ack()
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
    m = temp[2:-1].split('*@--')
    print(m[2])
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
    print(message)
    m = bytes(message, "utf-8")
    message = str(m)
    print(message)
    parity = 0
    p = 0
    for i in message[2:-1]:
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
    sock_send.sendto(bytes(message, "utf-8"), (UDP_IP_s_proxy, UDP_PORT_s_proxy))
    received = 0


def receive_http_ack():
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


def receive_http_proxy():
    global TCP_IP_s_server, sock_receive, sock_send
    sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock_receive.bind((UDP_IP_r_proxy, UDP_PORT_r_proxy))
    sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    hope = 1
    temp = receive_http_fragmented()
    if temp != str(-1):
        # print(temp)
        TCP_IP_s_server = str(temp[3])
        myMessage = str(temp[2])

        while temp[1] == str(1):
            temp = receive_http_fragmented()
            while temp == str(-1):
                print("parity error , remove the packet from buffer...")
                temp = receive_http_fragmented()
            if temp[0] == str(hope):
                myMessage += temp[2]
                hope += 1
        print("defragment finish")
        return myMessage
    else:
        print("parity error , remove the packet from buffer...")
    sock_receive.close()
    sock_send.close()

def receive_http_fragmented():
        print("client is waiting for response packet ...")
        notReceive = True
        while notReceive:
            data, addr = sock_receive.recvfrom(6500)  # buffer size is 6500 bytes
            print("receive packet")
            assert isinstance(data, object)
            print("received message:", data)
            notReceive = False

        if check_parity(data):
            print(data)
            temp = str(data)
            m = temp[2:-1].split('*@--')
            send_ack_http_proxy(data)
            return m
        else:
            print("parity error")
            return -1


def send_ack_http_proxy(data):
    print("send ack to proxy")
    global sock_send
    sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    print("UDP target IP:", UDP_IP_s_proxy)
    print("UDP target port:", UDP_PORT_s_proxy)
    print("message:", data)
    print("\n")
    sock_send.sendto(data, (UDP_IP_s_proxy, UDP_PORT_s_proxy))
    sock_send.close()


def save_result(result):
    f = codecs.open("index.html", "w", "utf-8")
    print(result)
    f.write(result)
    f.close()


def send_dns():
    print("send packet")
    print("DNS target IP:", TCP_IP_dns)
    print("DNS target port:", TCP_PORT)
    print("DNS target name:", TCP_Target)
    # print("message:", message)
    newmsg = bytes(DNS_type + "*@--" + TCP_IP_dns + "*@--" + TCP_Target , 'utf-8')
    d.connect((TCP_IP, TCP_PORT))
    d.send(newmsg)


def receive_dns():
    print("client waiting for answer ...")

    data = str(d.recv(BUFFER_SIZE))
    d.close()
    rcv_data = data[2:-1].split('*@--')
    target_ips = rcv_data[3]
    target_ips = target_ips.split('.@')
    print("recieved packet")
    print("DNS query type IP:", rcv_data[0])
    print("DNS query target names:", rcv_data[2])
    print("DNS query tareget Ips:", target_ips)
    show_result_dns(rcv_data)


def show_result_dns(message):
    print("received message:", message)


# DNS
TCP_IP = '127.0.0.1'
TCP_PORT = 5008
TCP_Target = 'mail.google.com'
DNS_type = 'A'  # CNAME
BUFFER_SIZE = 1024
# MESSAGE = "Hello, World!"

d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# HTTP
UDP_IP_s_proxy = "127.0.0.1"  # "185.211.88.22"
UDP_PORT_s_proxy = 5005
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
# receive part initiation
UDP_IP_r_proxy = "127.0.0.1"  # "185.211.88.22"
UDP_PORT_r_proxy = 5006
sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
TCP_IP_s_server = ""
received = 2  # 0 just send    1 receive ok   2 time out/send
DES_IP = "www.lifeHacker.com"
MESSAGE = "GET / HTTP/1.0\r\n\r\n"

# code section
x = input("please initialize client : ")
x = x.split(" ")
d = x[1].split("=")
temp = d[1].split(":")
tcpOrUdp = temp[0]
if tcpOrUdp == "tcp":
    #client –s=tcp:127.0.0.1:5008
    TCP_IP = str(temp[1])
    TCP_PORT = int(temp[2])
    TCP_Target = input("enter your target ")# 'mail.google.com'
    DNS_type =input("enter your query type") # 'A'  # CNAME
    TCP_IP_dns= input("enter your dns server IP") # 217.215.155.155
    BUFFER_SIZE = 1024
    # MESSAGE = "Hello, World!"

    d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_dns()
    receive_dns()
elif tcpOrUdp == "udp":
    UDP_IP_s_proxy = str(temp[1])
    UDP_PORT_s_proxy = int(temp[2])
    DES_IP = input("enter destionation IP : ")
    MESSAGE = input("enter message : ")
    # DES_IP = "www.lifeHacker.com"
    # MESSAGE = "GET / HTTP/1.0\r\n\r\n"
    if reliable_send(MESSAGE, DES_IP):
        print("send with no problem")
        result = receive_http_proxy()
        save_result(result)
    else:
        print("problem in udp sending...")
else:
    print(d)
    print("enter correct request")
    print("like : client –s=udp:127.0.0.1:80")



        # http type setting numberOfPacke * moreFragment * message * IPDestination * parity
#MESSAGE = input("enter your http message : ")
#DES_IP = "www.aut.ac.ir"
#MESSAGE = "GET / HTTP/1.0\r\n\r\n"