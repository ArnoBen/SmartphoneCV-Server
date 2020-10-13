import socket


def setup_communication(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    print("Waiting for connection...")
    conn, addr = s.accept()
    i = 0
    while True:
        try:
            print(f"Connection address: {addr}")
            data = conn.recv(BUFFER_SIZE)
            print("Received data: " + data.decode("utf8"))
            answer = f"Answer from server {i}"
            i += 1
            print("Sending: " + answer)
            conn.sendall(answer.encode("utf8"))
        except ConnectionError as error:
            print(f"CONNECTION ERROR : {error}")
            conn.close()
            s.close()
            break
        except ConnectionAbortedError as error:
            print(f"CONNECTION ABORTED ERROR {error}")
        except ConnectionRefusedError as error:
            print(f"CONNECTION REFUSED ERROR : {error}")
        except ConnectionResetError as error:
            print(f"CONNECTION RESET ERROR : {error}")

    setup_communication(host, port)


HOST, PORT = '', 9999
BUFFER_SIZE = 2 ** 14


print(f"Creating TCP server at {HOST}:{PORT}")

setup_communication(HOST, PORT)