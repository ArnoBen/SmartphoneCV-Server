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
        while True:
            self.data = self.request.recv(2**14)  # 2**14 = 16384 bytes
            decoded = cv2.imdecode(np.frombuffer(self.data, np.uint8), -1)
            if decoded is not None:
                print(f"Received image of resolution {decoded.shape}")
                cv2.imshow("Webcam", decoded)
                cv2.waitKey(1)
                print("Sending answer")
                self.request.sendall(f"Received image of shape {decoded.shape}".encode("utf-8"))
                return


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
"""


class DataProcessor:
    def __init__(self):
        self.expected_length = -1
        self.buffer = bytearray(b'')

    def process_data(self, data):
        # print(f"Received data of length {len(data)}")
        if data is None:  # return if no data
            return None
        else:
            # If the expected length is 0, data should be the length of the frame
            if self.expected_length == -1:
                try:
                    if data[:10].decode() == "datalength":
                        self.expected_length = int.from_bytes(data[10:14], byteorder='little')
                        # print(f"total length expected to be {self.expected_length}")
                        self.buffer.clear()
                    return None
                except UnicodeDecodeError:
                    print("data received does not follow the form 'datalengthXXXX'.")
                    return None
            # If it's not 0, we simply fill the buffer with the data being received
            else:
                self.buffer += data
                print(f"{len(self.buffer)}/{self.expected_length}")
                if len(self.buffer) == self.expected_length:
                    self.expected_length = -1
                    return self.process_full_buffer()
                elif len(self.buffer) > self.expected_length:  # There was an error during transfer
                    # clear everything and wait for next frame
                    print("buffer length over expected length")
                    self.expected_length = -1
                    self.buffer.clear()
                    return None
                else:  # Waiting for more data
                    return None


    def process_full_buffer(self):
        try:
            decoded = cv2.imdecode(np.frombuffer(self.buffer, np.uint8), -1)
            self.buffer.clear()
            decoded = cv2.rotate(decoded, cv2.ROTATE_90_CLOCKWISE)
            cv2.imshow("Webcam", decoded)
            cv2.waitKey(1)
            return f"Received image of resolution {decoded.shape}"
        except TypeError:
            error_feedback = "The data received is not an image"
            return error_feedback
        except cv2.error:
            error_feedback = "Problem encountered when decoding image"
            return error_feedback


if __name__ == "__main__":
    cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)

    HOST, PORT = '', 9999
    BUFFER_SIZE = 2 ** 16

    print(f"Creating TCP server at {HOST}:{PORT}")

    data_processor = DataProcessor()
    server = simple_server.Server(HOST, PORT, BUFFER_SIZE, data_processor)

    while True:
        user_input = input()
        server.send_data(user_input)
