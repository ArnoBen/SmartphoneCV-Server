import socket
import socketserver
import urllib.request
import dataprocessing
import json
import matplotlib.pyplot as plt
import numpy as np
import simple_server
import cv2
import yolov4


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(2 ** 15).strip()
        result = dataprocessing.data_processor.process_data(self.data)
        if result is not None:
            print("result : " + result)
            self.request.sendall(result)


if __name__ == "__main__":
    HOST, PORT = '', 10102
    BUFFER_SIZE = 2 ** 15

    print(f"Creating TCP server at {HOST}:{PORT}\n"
          f"Local IP : {socket.gethostbyname(socket.gethostname())}\n"
          f"Global IP : {urllib.request.urlopen('https://ident.me').read().decode('utf8')}")

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()