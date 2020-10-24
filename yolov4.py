import cv2
import time
import numpy as np
import json


class Info:
    def __init__(self, class_name, score, width, height, center):
        self.class_name = class_name
        self.score = score
        self.center = center
        self.width = width
        self.height = height



    def to_json(self):
        return json.dumps(self.as_dict())


class YoloDNN:
    def __init__(self):
        self.CONFIDENCE_THRESHOLD = 0.2
        self.NMS_THRESHOLD = 0.4
        self.COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
        self.class_names = []
        with open("yolo_config/coco.names", "r") as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

    def get_detections(self, frame):
        net = cv2.dnn.readNetFromDarknet("yolo_config/yolov4.cfg", "yolo_config/yolov4.weights")
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
        return self.get_infos_json(classes, boxes, scores, frame)

    def get_infos_json(self, classes, boxes, scores, frame):
        infos = []
        for i, class_id in enumerate(classes):
            class_name = self.class_names[class_id[0]]
            center_x, center_y, width, height = boxes[i]
            height = float(height / frame.shape[0]).__round__(3)
            width = float(width / frame.shape[1]).__round__(3)
            center_x = float(center_x / frame.shape[1]).__round__(3)
            center_y = float(center_y / frame.shape[0]).__round__(3)
            center = (center_x, center_y)
            score = float(scores[i][0]).__round__(3)
            info = Info(class_name, score, width, height, center)
            infos.append(info)
        infos_json = json.dumps([info.__dict__ for info in infos])
        return infos_json

# YoloDNN().get_detections(cv2.imread("picture.jpg"))