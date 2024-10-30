import os
import cv2
import numpy as np
from Biotreasure.settings import MEDIA_ROOT
from ultralytics import YOLO

class ObjectDetector():

    def __init__(self):
        local      = os.path.join(MEDIA_ROOT,'modelo','best.pt')
        self.model = YOLO(local)  # ou 'yolov8' dependendo da versão


    def predict(self, img_path):
        results = self.model(img_path)
        return results

    def draw_boxes(self, img_path, results):
        img = cv2.imread(img_path)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = f"{result.names[box.cls.detach().cpu().numpy()[0]]}"
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
        cv2.imwrite(img_path, img)