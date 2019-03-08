import sys
import socket
import getopt
import threading
import subprocess

# define globals
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

# function to handle CLI arguments
def usage():

    explanation = """  BHP Net Tool
    
                Usage: bhpnet.py -t target_host -p port
                -l --listen              - listen on [host]:[port] for incoming connections
                -e --execute=file_to_run - execute the given file upon receiving a connection
                -c --command             - initialize a command shell
                -u --upload=destination  - upon receiving connection upload a file and write to [destination]
                
                Examples:
                bhpnet.py -t 182.168.0.1 -p 5555 -l -c
                bhpnet.py -t 182.168.0.1 -p 5555 -l -u=c:\\target.exe
                bhpnet.py -t 182.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"""
                echo 'ABCD' | ./bhpnet.py -t 192.168.11.12 -p 135
    """

    print(explanation)

def read_cli_options():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])

        return opts, args
    except getopt.GetoptError as error:
        print(str(error))
        usage()

def client_sender(buffer):

    # AF_INET means IPv4 address
    # SOCK_STREAM means TCP client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to target host
        client.connect((target, port))

        # Test to see if any input from stdin
        if len(buffer):
            client.send(buffer)

        # now we need to wait for our data to come back
        while True:

            recv_len = 1
            response = ""

            while recv_len:

                # Max data size of 4096
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                # if we receive less than 4096 bytes, stop receiving
                if recv_len < 4096:
                    break

            print(response)

            # Wait for more input
            buffer = input("")
            buffer += "\n"

            # send it away
            client.send(buffer)

    except:
        print("[*] Exception! Exiting")

        # tear down the connection
        client.close()

def server_loop():
    global target

    # if no target is defined, listen on all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, )


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # Read CLI options
    opts, args = read_cli_options()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination
        elif o in ("-t", "--target"):
            target = a
        else:
            assert False, "Unhandled Option"

    # Mimic Netcat to read data from stdin and send it across the network.
    # If we are not listening and just sending data
    if not listen and len(target) and port > 0:

        # read buffer from CLI
        # Send CTRL-D if not sending input to stdin
        buffer = sys.stdin.read()

        # send the data
        client_sender(buffer)

    # if we are listening, we may need to upload things, execute commands, drop a shell back
    if listen:
        server_loop()


main()
