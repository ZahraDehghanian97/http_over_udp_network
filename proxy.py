import socket


# function part
def receive_http():
    hope = 1
    temp = receive_http_fragmented()
    TCP_IP_s_server = str(temp[3])
    myMessage = str(temp[2])
    while temp[1] == str(1):
        temp = receive_http_fragmented()
        if temp[0] == str(hope):
            myMessage += temp[2]
            hope += 1
    print("defragment finish")
    return myMessage


def receive_http_fragmented():
    sock_r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock_r.bind((UDP_IP_r_client, UDP_PORT_r_client))
    print("proxy is waiting for packet ...")
    notReceive = True
    while notReceive:
        data, addr = sock_r.recvfrom(1024)  # buffer size is 1024 bytes
        print("receive packet")
        assert isinstance(data, object)
        print("received message:", data)
        notReceive = False
    if check_parity(data):
        temp = str(data)
        m = temp[2:-1].split('*')
        send_http(data)
        return m
    else:
        return -1
    sock_r.close()


def send_http(data):
    sock_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    print("UDP target IP:", UDP_IP_s_client)
    print("UDP target port:", UDP_PORT_s_client)
    print("message:", data)
    print("\n")
    sock_s.sendto(data, (UDP_IP_s_client, UDP_PORT_s_client))
    sock_s.close()


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


#
# def send_http_server(data):
#
# def receive_http_server():


TCP_port_s_server = 80
TCP_IP_s_server = ""
UDP_IP_r_client = "127.0.0.1"
UDP_PORT_r_client = 5005
UDP_IP_s_client = "127.0.0.1"  # "185.211.88.22"
UDP_PORT_s_client = 5006
# receive part
while 1:
    message = receive_http()
    print(message)
# send_http_server(data)
# data = receive_http_server()
# send_http(message)

# http type setting numberOfPacke * moreFragment * message * IPDestination * parity
