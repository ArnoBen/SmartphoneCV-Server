import socket
HOST, PORT = 'localhost', 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

try:
    data = "Message from client"
    print("Sending: " + data)
    data = data.encode("utf8")
    s.sendall(data)
except ConnectionRefusedError:
    print("Connexion failed")

data = s.recv(256)
print("Received response : " + data.decode("utf8"))

s.close()