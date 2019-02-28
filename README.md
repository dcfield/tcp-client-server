# TCP Server and Client
TCP servers can be used for writing command shells or creating a proxy.

## Pre-requisites
- python 3

## Download
- git clone https://github.com/dcfield/tcp-client-server.git

## Start your TCP server
- Open a terminal.
- `python3 ./tcp-server.py`
- You should get the message `[*] listening on 0.0.0.0:9999`.

## Start your TCP client
- Open a *new* terminal
- `python3 ./tcp-client.py`
- Your TCP client terminal should receive a message from the server: `b'ack!'`
- Your TCP server should confirm where it accepted the request from, and what it received.

## Experiment
- Play around with both TCP client and server to see how you can break it or get it to send different responses.

