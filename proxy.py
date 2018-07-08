import socket


UDP_IP_r = "127.0.0.1"
UDP_PORT_r = 5005
UDP_IP_s = "127.0.0.1"  # "185.211.88.22"
UDP_PORT_s = 5006
# receive part
while 1:
    sock_r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock_r.bind((UDP_IP_r, UDP_PORT_r))
    print("proxy is waiting for packet ...")
    notReceive = True
    while notReceive:
        data, addr = sock_r.recvfrom(1024)  # buffer size is 1024 bytes
        print("receive packet")
        assert isinstance(data, object)
        print("received message:", data)
        notReceive = False
    sock_r.close()
    # send part

    sock_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    print("UDP target IP:", UDP_IP_s)
    print("UDP target port:", UDP_PORT_s)
    print("message:", data)
    print("\n")
    sock_s.sendto(data, (UDP_IP_s, UDP_PORT_s))
    sock_s.close()