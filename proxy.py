import dns.resolver
import socket
import select
import requests


# HTTP
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
        print("parity error , remove the packet from buffer...")


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
        m = temp[2:-1].split('*@--')
        sock_c.close()
        send_ack_http_client(data)
        return m
    else:
        sock_c.close()
        return -1


def send_ack_http_client(data):
    sock_c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    # print("UDP target IP:", UDP_IP_s_client)
    # print("UDP target port:", UDP_PORT_s_client)
    # print("message:", data)
    # print("\n")
    sock_c.sendto(data, (UDP_IP_s_client, UDP_PORT_s_client))
    sock_c.close()


def reliable_send_client(message, ip):
    print("***********")
    print("reliable send to client ")
    print("***********")
    global received
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
        FragmentedMESSAGE = str(x) + '*@--' + str(fragment) + '*@--' + message[start: end] + '*@--' + str(
            ip) + "*@--" + make_parity(message[start: end])
        print("send packet : " + FragmentedMESSAGE)
        if reliable_send_fragmented(FragmentedMESSAGE):
            print("send succsecfully packet : " + str(x))
            print("\n")
            x += 1
            received = 2
        else:
            print("can not send response to client, error occurred in packet number " + str(x))
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
        print("client is not ready to receive answer")
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
    sock_send_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # print("send packet")
    # print("UDP target IP:", UDP_IP_s)
    # print("UDP target port:", UDP_PORT_s)
    # print("message:", message)
    sock_send_client.sendto(bytes(message, "utf-8"), (UDP_IP_s_client, UDP_PORT_s_client))
    received = 0
    sock_send_client.close()


def receive_http():
    global received
    sock_receive_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock_receive_client.bind((UDP_IP_r_client, UDP_PORT_r_client))
    sock_receive_client.setblocking(0)
    print("proxy waiting for ack from client ...")
    ready = select.select([sock_receive_client], [], [], 1)
    if ready[0]:
        receive_data, addr = sock_receive_client.recvfrom(6500)  # buffer size is 1024 bytes
        sock_receive_client.close()
        if check_parity(receive_data):
            received = 1
            assert isinstance(receive_data, object)
            # print(receive_data)
            return receive_data
        else:
            received = 2
            print("parity error")
            return 0

    else:
        received = 2
        print("time out ")
        sock_receive_client.close()
        return 0


def check_parity(message):
    # m[2] data - m[4] parity
    print(message)
    temp = str(message)
    m = temp[2:-1].split('*@--')
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


def send_and_receive_http_server(message):
    global TCP_IP_s_server, TCP_port_s_server, BUFFER_SIZE, data
    print("send request to : ", TCP_IP_s_server, " on port : ", TCP_port_s_server)
    sock_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_s.connect((TCP_IP_s_server, TCP_port_s_server))
    if message == "GET / HTTP/1.0\\r\\n\\r\\n":
        sock_s.send(bytes("GET / HTTP/1.0\r\n\r\n", 'utf-8'))
    else:
        sock_s.send(bytes(message, 'utf-8'))
    print("proxy waiting for answer from internet ...")
    # ans = bytes('',"utf-8")
    # isNotFinished = True
    # while isNotFinished :
    # print("here")
    # t = sock_s.recv(BUFFER_SIZE)
    temp = "http://"
    temp = temp + TCP_IP_s_server
    t = requests.get(temp)
    answer = t.text
    data = answer
    # print(data)
    type = t.status_code
    sock_s.close()
    if type == "200":
        print("200 receive answer with no problem ")
        return data
    elif type == "404":
        print("404 not found")
        return data
    elif type == "403":
        print("403 forbidden")
        return data
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
    else:
        return data


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


# DNS

def receive_dns_client():
    global msg
    print("proxy waiting for dns query ...")
    d.bind((TCP_IP, TCP_PORT))
    d.listen(1)
    conn, addr = d.accept()
    print('Connection address:', addr)
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print("received data:", data)
        msg = str(data)
        # tmp = str(msg)
        msg = msg[2:-1].split('*@--')
        show_result_dns(msg)
        data = findAnswer("dns", msg)
        print("final data" + data)
        data = bytes(data, 'utf-8')
        conn.send(data)  # echo
    conn.close()

    show_result_dns(msg)

    # return m


def send_dns_server_udp(dns_query):
    ip_addr = ""
    myResolver = dns.resolver.Resolver()  # create a new instance named 'myResolver'
    myResolver.timeout = 0.01
    if dns_query[0] == "A":
        if "www" in dns_query[2]:
            dns_query[2] = dns_query[2][3:].split("www")
        print(dns_query[2])
        ip_addr = socket.gethostbyname(dns_query[2])
        print(ip_addr)  # print IP address
    elif dns_query[0] == "CNAME":
        answers = myResolver.query(dns_query[2], 'CNAME')
        print(' query qname:', answers.qname, ' num ans.', len(answers))
        for rdata in answers:
            ip_addr = str(ip_addr + str(rdata.target) + "@")
            # print(' cname target address:', rdata.target + "@")

            # info= socket.gethostbyname_ex(dns_query[2])
            # ip_addr = info[2]
    send_data = send_dns_client_tcp(ip_addr)
    print(send_data)
    return send_data


def send_dns_client_tcp(MESSAGE_IP):
    print("send packet from proxy")
    print("DNS target IP:", TCP_IP)
    print("DNS target port:", TCP_PORT)
    print("DNS target name:", msg[2])
    # print("message:", msg[3])
    newmsg = str(msg[0] + "*@--" + TCP_IP + "*@--" + msg[2] + "*@--" + MESSAGE_IP)
    print("send_dns_server_udp" + newmsg)
    return newmsg


def show_result_dns(message):
    print("received message:", message)


def findAnswer(type, msg):
    global turn
    flag = True
    if turn == 10:
        turn = 0
    for i in cache:
        if msg in i:
            print("find result in cache ... ")
            flag = False
            return i[1]

    if flag:
        print("result did not find in cache ... ")
        print("we send your request to server ")
        if type == "dns":
            ans = send_dns_server_udp(msg)
        if type == "http":
            ans = send_and_receive_http_server(msg)
        if len(cache) < 10:
            cache.append([msg, ans])
            return ans
        elif len(cache) == 10:
            del cache[turn]
            cache.insert(turn, [msg, ans])
            turn += 1
            return ans


# DNS

TCP_IP = '127.0.0.1'
TCP_PORT = 5008
BUFFER_SIZE = 1024

# d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# receive_dns_client()

# HTTP
TCP_port_s_server = 80
TCP_IP_s_server = ""
UDP_IP_r_client = "127.0.0.1"
UDP_PORT_r_client = 5005
UDP_IP_s_client = "127.0.0.1"  # "185.211.88.22"
UDP_PORT_s_client = 5006
BUFFER_SIZE = 10000
received = 2
data = ""
turn = 0
cache = []

d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


x = input()
x = x.split(" ")
d = x[1].split("=")
temp = d[1].split(":")
tcpOrUdp = temp[0]
if tcpOrUdp == "tcp":
    TCP_IP = str(temp[1])
    TCP_PORT = int(temp[2])
    receive_dns_client()
elif tcpOrUdp == "udp":
    UDP_IP_r_client = str(temp[1])
    UDP_PORT_r_client = int(temp[2])
    message = receive_http_client()
    data = findAnswer("http", message)
    # print("receive message from server : ", data)
    reliable_send_client(str(data), TCP_IP_s_server)
else:
    print(d)
    print("enter correct request")
    print("like : proxy –s=udp:127.0.0.1:80 –d=tcp")


        # http type setting numberOfPacke * moreFragment * message * IPDestination * parity
