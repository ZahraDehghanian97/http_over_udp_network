import socket
#import dns  #import the module

def receive_dns_client():
    global mahin
    print("client waiting for answer ...")

    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()
    print('Connection address:', addr)
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print("received data:", data)
        mahin = data
        conn.send(data)  # echo
    conn.close()

    show_result_dns(mahin)
    tmp = str(mahin)
    m = tmp[2:-1].split('*')
    return m

def send_dns_server(hostname):
    print(hostname)
    ip_addr1 = socket.gethostbyname(hostname)
   # addr2 = socket.gethostbyname('yahoo.com')

    print(ip_addr1) # print IP address



# def reliable_send_server_udp(message):
#     counter = 0
#     global received
#     while counter < 15:
#         if received == 0:
#             result = receive_dns_client()
#         if received == 1:
#             counter = 15
#             return True
#         if received == 2:
#             sen(message)
#             counter += 1

    # if counter == 15 and received == 2:
    #     print("server is not available")
    #     return False


def show_result_dns(message):
    print("received message:", message)




TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dns_query = receive_dns_client()
if "www" in dns_query[2] :
    dns_query[2]= dns_query[2][3:].split("www")

send_dns_server(dns_query[2])



# myResolver = dns.resolver.Resolver() #create a new instance named 'myResolver'
# myAnswers = myResolver.query("google.com", "A") #Lookup the 'A' record(s) for google.com
# for rdata in myAnswers: #for each response
#     print rdata #print the data
#

