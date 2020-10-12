import socket
import socketserver
import json
import matplotlib.pyplot as plt
import numpy as np
import cv2


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(2 ** 14)  # 2**14 = 16384 bytes
        decoded = cv2.imdecode(np.frombuffer(self.data, np.uint8), -1)
        if decoded is not None:
            print(f"Received image of resolution {decoded.shape}")
            cv2.imshow("Webcam", decoded)
            cv2.waitKey(1)
            self.request.sendall(f"Received image of shape {decoded.shape}".encode("utf-8"))
            return

def display_image(data):
    img = np.reshape(data, ())


if __name__ == "__main__":
    HOST, PORT = socket.gethostbyname(socket.gethostname()), 9999
    print("Socket at IP " + HOST)

    cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer(("localhost", PORT), MyTCPHandler)
    # server.server_close()
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()