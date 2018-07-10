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
    sock_c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock_c.bind((UDP_IP_r_client, UDP_PORT_r_client))
    print("proxy is waiting for packet ...")
    notReceive = True
    while notReceive:
        data, addr = sock_c.recvfrom(1024)  # buffer size is 1024 bytes
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
    sock_c.close()


def send_http_client(data):
    sock_c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    # print("UDP target IP:", UDP_IP_s_client)
    # print("UDP target port:", UDP_PORT_s_client)
    # print("message:", data)
    # print("\n")
    message = "http*" + data
    sock_c.sendto(bytes(message, 'utf-8'), (UDP_IP_s_client, UDP_PORT_s_client))
    sock_c.close()


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
    print("send request to : ", TCP_IP_s_server, " on port : ", TCP_port_s_server)
    sock_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.getaddrinfo('127.0.0.1', 8080)
    sock_s.connect((TCP_IP_s_server, TCP_port_s_server))
    if message == "GET / HTTP/1.0\\r\\n\\r\\n":
        sock_s.send(bytes("GET / HTTP/1.0\r\n\r\n", 'utf-8'))
    else:
        sock_s.send(bytes(message, 'utf-8'))


def receive_http_server():
    print("proxy waiting for answer from internet ...")
    data = sock_s.recv(BUFFER_SIZE)
    print(data)
    return data


def send_and_receive_http_server(message):
    global TCP_IP_s_server, sock_s
    print("i am here")
    send_http_server(message)
    ans = receive_http_server()
    print(ans)
    temp = str(ans)
    temp = temp.split('\'')
    answer = temp[1].split(' ')
    type = answer[1]
    print(type)
    if type == "200":
        print("200 receive answer with no problem ")
        return ans

    elif type == "404":
        print("404 not found")
        return ans
    elif type == "403":
        print("403 forbidden")
        return ans
    elif type == "301" or type == "302":
        print("301/302 move temporarily")
        for i in answer:
            if 'Location:' in i:
                # print(splitedData[splitedData.index(i) + 1])
                new_location = answer[answer.index(i) + 1]
                new_location = new_location.split('//')
                new_location = new_location[1].split('\\')
                TCP_IP_s_server = new_location[0]
                make_ready_ip(TCP_IP_s_server, message)


def make_ready_ip(ip, message):
    global TCP_IP_s_server
    temp = ip.split('/')
    TCP_IP_s_server = temp[0]
    s = ""
    for i in range(1, len(temp)):
        s += '/' + temp[i]
    if message == "GET / HTTP/1.0\\r\\n\\r\\n":
        m = "GET " + s + " HTTP/1.0\r\n\r\n"
    else:
        m = message
    print(m)
    send_and_receive_http_server(m)


TCP_port_s_server = 80
TCP_IP_s_server = ""
UDP_IP_r_client = "127.0.0.1"
UDP_PORT_r_client = 5005
UDP_IP_s_client = "127.0.0.1"  # "185.211.88.22"
UDP_PORT_s_client = 5006
BUFFER_SIZE = 2048

while 1:
    sock_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.getaddrinfo('127.0.0.1', 8080)
    message = receive_http_client()
    print("now we send your request to server ")
    data = send_and_receive_http_server(message)
    send_http_client(data)
    # sock_s.close()

# http type setting numberOfPacke * moreFragment * message * IPDestination * parity
