from ultralytics import YOLO
from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2

model = YOLO('yolov8n.pt')
#model = YOLO('yolov8m.pt')

#results = model('traffic-detection-test.jpg', save=True)

#print(results[0].boxes)

print(model.names)