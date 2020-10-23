import cv2
import time
import numpy as np
import json


class Info:
    def __init__(self, class_name, score, width, height, center):
        self.class_name = class_name
        self.score = score
        self.center = center
        self.width = widtha
        self.height = height

    def as_dict(self):
        return {'Class': self.class_name,
                'Score': self.score,
                'Center': self.center,
                'Width': self.width,
                'Height': self.height}

    def to_json(self):
        return json.dumps(self.as_dict(), default=lambda o: str(o), sort_keys=True, indent=4)


class YoloDNN:
    def __init__(self):
        self.CONFIDENCE_THRESHOLD = 0.2
        self.NMS_THRESHOLD = 0.4
        self.COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
        self.class_names = []
        with open("yolo_config/coco.names", "r") as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

    def get_detections(self, frame):
        net = cv2.dnn.readNetFromDarknet("yolo_config/yolov4-tiny.cfg", "yolo_config/yolov4-tiny.weights")
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(416, 416), scale=1 / 255)

        start = time.time()
        classes, scores, boxes = model.detect(frame, self.CONFIDENCE_THRESHOLD, self.NMS_THRESHOLD)
        end = time.time()

        start_drawing = time.time()
        for (classid, score, box) in zip(classes, scores, boxes):
            color = self.COLORS[int(classid) % len(self.COLORS)]
            label = "%s : %f" % (self.class_names[classid[0]], score)
            cv2.rectangle(frame, box, color, 2)
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        end_drawing = time.time()

        fps_label = "FPS: %.2f (excluding drawing time of %.2fms)" % (
        1 / (end - start), (end_drawing - start_drawing) * 1000)
        cv2.putText(frame, fps_label, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow("detections", frame)
        cv2.waitKey(1)
        return json.dumps(self.get_info(classes, boxes, scores, frame))

    def get_info(self, classes, boxes, scores, frame):
        infos = []
        for i, class_id in enumerate(classes):
            class_name = self.class_names[class_id[0]]
            center_x, center_y, width, height = boxes[i]
            height /= frame.shape[0]
            width /= frame.shape[1]
            center_x /= frame.shape[0]
            center_y /= frame.shape[1]
            center = (center_x, center_y)
            info = Info(class_name, scores[i][0], width, height, center)
            infos.append(info)
        json.dumps([i.to_json() for i in infos])
        return infos

YoloDNN().get_detections(cv2.imread("picture.jpg"))