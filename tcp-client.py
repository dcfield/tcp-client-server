import socket

target_host = "127.0.0.1"
target_port = 9999

# create a socket object
# AF_INET means IPv4 address
# SOCK_STREAM means TCP client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client to the target host
client.connect((target_host, target_port))

# send some dummy data
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# receive some data with buffer size 4096
response = client.recv(4096)

print(response)

