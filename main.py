import socket
import socketserver
import json
import matplotlib.pyplot as plt
import numpy as np
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


def send_message():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.0.75", 9999))
    s.send("some message".encode("utf-8"))
    # I think it can receive. See https://wiki.python.org/moin/TcpCommunication
    data = s.recv(1024)
    s.close()
    print(f"received data of length {len(data)}")


if __name__ == "__main__":
    HOST, PORT = '', 9999
    BUFFER_SIZE = 2 ** 14
    print("Socket at IP " + HOST)

    cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    # server.server_close()
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

#endregion
"""
