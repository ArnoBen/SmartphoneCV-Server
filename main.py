import socket
import socketserver
import json
import matplotlib.pyplot as plt
import numpy as np
import simple_server
import cv2
import yolov4


class DataProcessor:
    def __init__(self):
        self.expected_length = -1
        self.buffer = bytearray(b'')
        self.yolo_model = yolov4.YoloDNN()

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
            #decoded = cv2.rotate(decoded, cv2.ROTATE_90_CLOCKWISE)
            self.yolo_model.get_detections(decoded)
            return f"Received image of resolution {decoded.shape}"
        except TypeError:
            error_feedback = "The data received is not an image"
            return error_feedback
        except cv2.error:
            error_feedback = "Problem encountered when decoding image"
            return error_feedback


if __name__ == "__main__":
    HOST, PORT = '', 9999
    BUFFER_SIZE = 2 ** 16

    print(f"Creating TCP server at {HOST}:{PORT}")

    data_processor = DataProcessor()
    server = simple_server.Server(HOST, PORT, BUFFER_SIZE, data_processor)