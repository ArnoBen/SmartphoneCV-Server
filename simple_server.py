import socket


class Server:
    host = None
    port = None
    buffer_size = 1024
    s = None
    conn = None

    def __init__(self, _host, _port, _buffer_size, data_processor):
        self.host = _host
        self.port = _port
        self.buffer_size = _buffer_size
        self.setup_communication(data_processor)


    def setup_communication(self, data_processor):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen()
        print("Waiting for connection...")
        conn, addr = s.accept()
        i = 0
        while True:
            try:
                print(f"Connection address: {addr}")
                data = conn.recv(self.buffer_size)
                data_processor(data)
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

        self.setup_communication(data_processor)

    def send_data(self, data):
        try:
            self.conn.sendall(data)
        except ConnectionError as error:
            print(f"CONNECTION ERROR : {error}")