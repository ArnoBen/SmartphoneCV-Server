import socket

HOST, PORT = '', 9999
BUFFER_SIZE = 2 ** 14

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print(f"Creating TCP server at {HOST}:{PORT}")

while True:
    s.listen()
    conn, addr = s.accept()
    print(f"Connection address: {addr}")
    data = conn.recv(BUFFER_SIZE)
    print(data.decode("utf8"))
    answer = "Answer from server"
    print("Sending: " + answer)
    conn.sendall(answer.encode("utf8"))

conn.close()
socket.close()
