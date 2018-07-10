import socket


# function part
def receive_http_client():
    global TCP_IP_s_server
    hope = 1
    temp = receive_http_fragmented()
    if temp != str(-1):
        # print(temp)
        TCP_IP_s_server = str(temp[3])
        myMessage = str(temp[2])
        while temp[1] == str(1):
            temp = receive_http_fragmented()
            if temp[0] == str(hope):
                myMessage += temp[2]
                hope += 1
        print("defragment finish")
        return myMessage
    else:
        print("parity ertot , remove the packet from buffer...")


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
        print(data)
        temp = str(data)
        m = temp[2:-1].split('*')
        send_http_client(data)
        return m
    else:
        return -1
    sock_r.close()


def send_http_client(data):
    sock_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    print("UDP target IP:", UDP_IP_s_client)
    print("UDP target port:", UDP_PORT_s_client)
    print("message:", data)
    print("\n")
    sock_s.sendto(data, (UDP_IP_s_client, UDP_PORT_s_client))
    sock_s.close()


def check_parity(message):
    # m[2] data - m[4] parity
    print(message)
    temp = str(message)
    m = temp[2:-1].split('*')
    p = 0
    print(m[2])
    for i in m[2]:
        p += ord(i)
    parity = bin(p)
    parity = parity.split('b')
    print(m[4], "compare to ", parity[1])
    if m[4] == parity[1]:
        return True
    else:
        return False


def send_http_server(message):
    global sock_s
    print(TCP_IP_s_server,TCP_port_s_server)
    assert isinstance(sock_s, object)
    sock_s.connect((TCP_IP_s_server, TCP_port_s_server))
    print(message, "and GET / HTTP/1.0\\\r\\\n\\\r\\\n")
    if message == "GET / HTTP/1.0\\r\\n\\r\\n":
        print("send in if")
        sock_s.send(bytes("GET / HTTP/1.0\r\n\r\n", 'utf-8'))
    else:
        print("send in else")
        sock_s.send(bytes(message, 'utf-8'))


def receive_http_server():
    print("proxy waiting for answer from internet ...")
    data = sock_s.recv(BUFFER_SIZE)
    print(data)
    return data


def send_and_receive_http_server(message):
    global TCP_IP_s_server,sock_s
    print("i am here")
    send_http_server(message)
    ans = receive_http_server()
    print(ans)
    temp = str(ans)
    temp = temp.split('\'')
    answer = temp[1].split(' ')
    type = answer[1]
    if type == "200":
        print("200 receive answer with no problem ")
        return ans

    if type == "404":
        print("404 not found")
        return ans
    if type == "301" or type == "302":
        print("301/302 move temporarily")
        for i in answer:
            if 'Location:' in i:
                # print(splitedData[splitedData.index(i) + 1])
                new_location = answer[answer.index(i) + 1]
                new_location = new_location.split('//')
                new_location = new_location[1].split('\\')
                TCP_IP_s_server = new_location[0]
                print(TCP_IP_s_server)
                sock_s.close()
                sock_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                send_and_receive_http_server(message)


TCP_port_s_server = 80
TCP_IP_s_server = ""
UDP_IP_r_client = "127.0.0.1"
UDP_PORT_r_client = 5005
UDP_IP_s_client = "127.0.0.1"  # "185.211.88.22"
UDP_PORT_s_client = 5006
BUFFER_SIZE = 2048

while 1:
    sock_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    message = receive_http_client()
    print("now we send message to server in main  ", message)
    data = send_and_receive_http_server(message)
    # send_http_server(message)
    # data = receive_http_server()
    send_http_client(data)
    # sock_s.close()

# http type setting numberOfPacke * moreFragment * message * IPDestination * parity
