import socket


def receive_dns_client():
    global msg
    print("proxy waiting for dns query ...")
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()
    print('Connection address:', addr)
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print("received data:", data)
        msg = str(data)
        # tmp = str(msg)
        msg = msg[2:-1].split('*')
        show_result_dns(msg)
        data = send_dns_server_udp(msg)
        print("final data" + data)
        data = bytes(data, 'utf-8')
        conn.send(data)  # echo
    conn.close()

    show_result_dns(msg)

    # return m


def send_dns_server_udp(dns_query):

    if dns_query[0] == "A":
        if "www" in dns_query[2]:
            dns_query[2] = dns_query[2][3:].split("www")
        print(dns_query[2])
        ip_addr = socket.gethostbyname(dns_query[2])
        print(ip_addr)  # print IP address
    elif dns_query[0] == "CNAME":
         ip_addr= socket.gethostbyname_ex(dns_query[2])
    send_data = send_dns_client_tcp(ip_addr)
    print(send_data)  # print IP address
    return send_data


def send_dns_client_tcp(MESSAGE_IP):
    print("send packet from proxy")
    print("DNS target IP:", TCP_IP)
    print("DNS target port:", TCP_PORT)
    print("DNS target name:", msg[2])
    # print("message:", msg[3])
    newmsg = str(msg[0] + "*" + TCP_IP + "*" + msg[2] + "*" + MESSAGE_IP)
    print("send_dns_server_udp" + newmsg)
    return newmsg


def show_result_dns(message):
    print("received message:", message)


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receive_dns_client()
