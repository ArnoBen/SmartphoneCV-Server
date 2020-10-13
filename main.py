import socket
import socketserver
import json
import matplotlib.pyplot as plt
import numpy as np
import simple_server
import cv2

"""
#region MainScript

class MyTCPHandler(socketserver.BaseRequestHandler):
    # The request handler class for our server.
    #
    # It is instantiated once per connection to the server, and must
    # override the handle() method to implement communication to the
    # client.

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(BUFFER_SIZE)  # 2**14 = 16384 bytes
        decoded = cv2.imdecode(np.frombuffer(self.data, np.uint8), -1)
        if decoded is not None:
            print(f"Received image of resolution {decoded.shape}")
            cv2.imshow("Webcam", decoded)
            cv2.waitKey(1)
            print("Sending answer")
            self.request.sendall(f"Received image of shape {decoded.shape}".encode("utf-8"))
            return
"""


def process_data(data):
    print(f"Received data of length {len(data)}")
    return f"Received data of length {len(data)}"
    # decoded = cv2.imdecode(np.frombuffer(data, np.uint8), -1)
    # if decoded is not None:
    #     print(f"Received image of resolution {decoded.shape}")
    #     cv2.imshow("Webcam", decoded)
    #     cv2.waitKey(1)


if __name__ == "__main__":
    HOST, PORT = '', 9999
    BUFFER_SIZE = 2 ** 14

    print(f"Creating TCP server at {HOST}:{PORT}")

    server = simple_server.Server(HOST, PORT, BUFFER_SIZE, process_data)

    while True:
        user_input = input()
        server.send_data(user_input)
    # cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)
