"""
To be used for writing command shells or a proxy.
This is a standard multi-threaded TCP server.
"""

import socket
import threading

# 0.0.0.0 tells the server to listen on every available network interface
bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# pass in IP and port we want the server to listen on
server.bind((bind_ip, bind_port))

# Tell server to start listening
# Max backlog of connections = 5
server.listen(5)

print("[*] listening on %s:%d" % (bind_ip, bind_port))

# Create client handling
def handle_client(client_socket):

    # print whatever the client sends
    request = client_socket.recv(1024)

    print("[*] Received: %s" % request)

    # send back a packet
    client_socket.send(b"ACK!")

    client_socket.close()

# Tell server to wait on a loop for incoming connections
while True:

    # client connect and
    # client stores client socket
    # addr stores remote connection details
    client, addr = server.accept()

    print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

    # bring up client thread to handle incoming data
    # point to 'handle_client' and pass in client socket object as argument
    client_handler = threading.Thread(target=handle_client, args=(client,))

    # start thread to handle client connection
    client_handler.start()
