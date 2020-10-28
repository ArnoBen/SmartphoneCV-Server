import yolov4
import cv2
import numpy as np


class DataProcessor:
    def __init__(self):
        self.expected_length = -1
        self.buffer = bytearray(b'')
        self.yolo_model = yolov4.YoloDNN()
        self.from_smartphone = False

    def process_data(self, data):
        if data is None:  # return if no data
            return None
        else:
            # If the expected length is 0, data should be the length of the frame
            if self.expected_length == -1:
                try:
                    if data[:11].decode() == "information":
                        self.from_smartphone = True if data[11] == 1 else False
                        self.expected_length = int.from_bytes(data[12:16], byteorder='little')
                        print(f"total length expected to be {self.expected_length}")
                        self.clear_buffer()
                    return None
                except UnicodeDecodeError:
                    print("data received does not follow the form 'informationXXXX'.")
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
                    self.clear_buffer()
                    return "error~buffer overflow"
                else:  # Waiting for more data
                    return None

    def process_full_buffer(self):
        frame = self.decode_image()
        info_json = self.yolo_model.get_detections(frame)
        return info_json  # f"Received image of resolution {decoded.shape}"

    def clear_buffer(self):
        self.buffer.clear()

    def decode_image(self):
        try:
            decoded = cv2.imdecode(np.frombuffer(self.buffer, np.uint8), -1)
            self.buffer.clear()
            if self.from_smartphone:
                decoded = cv2.rotate(decoded, cv2.ROTATE_90_CLOCKWISE)
            return decoded
        except TypeError:
            error_feedback = "The data received is not an image"
            return error_feedback
        except cv2.error:
            error_feedback = "Problem encountered when decoding image"
            return error_feedback


data_processor = DataProcessor()