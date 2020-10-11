import socket
import socketserver
import json
import matplotlib.image as mpimg
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
        self.data = self.request.recv(2**14) # 2**14 = 16384 bytes
        decoded = cv2.imdecode(np.frombuffer(self.data, np.uint8), -1)
        if decoded is not None:    
            print(f"Received image of resolution {decoded.shape}")
            cv2.imshow("Webcam", decoded)
            cv2.waitKey(1)
            return
        #cv.imshow("received frame", decoded)
        
        # print("{} wrote:".format(self.client_address[0]))
        # print(len(self.data))
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())


def display_image(data):
    img = np.reshape(data, ())


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    #server.server_close()
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
#
#class Sender:
#    def __init__(self):     
#        self.sock = socket.socket(socket.AF_INET, # Internet
#                         socket.SOCK_DGRAM) # UDP
#    def send(self, data, adress = "127.0.0.1", port = 9999):
#        self.sock.sendto(json.dumps(data).encode(), (adress, port))
#        
#class Receiver:
#    def __init__(self):
#        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    
#    def send(self, msg):
#        totalsent = 0
#        while totalsent < MSGLEN:
#            sent = self.sock.send(msg[totalsent:])
#            if sent == 0:
#                raise RuntimeError("socket connection broken")
#            totalsent = totalsent + sent
#
#    def receive(self):
#        chunks = []
#        bytes_recd = 0
#        MSGLEN = 2;
#        while bytes_recd < MSGLEN:
#            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
#            if chunk == b'':
#                raise RuntimeError("socket connection broken")
#            chunks.append(chunk)
#            bytes_recd = bytes_recd + len(chunk)
#        return b''.join(chunks)
#    
#    