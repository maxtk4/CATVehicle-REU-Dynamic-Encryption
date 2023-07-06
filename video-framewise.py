"""
current error msg:

cv2 cannot get video stream from IMG_2022.mpg

"""


from ultralytics import YOLO
import cv2
import torch

import cv2
cap = cv2.VideoCapture('IMG_2022.mpg')
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#create a window to display the img
cv2.namedWindow('mywindow')

cv2.waitKey()

#open the capture
while cap.isOpened():
    err,img = cap.read()

    #if we have run out of frames to process, exit
    if cap.get(cv2.CAP_PROP_POS_FRAMES) >= cv2.CAP_PROP_FRAME_COUNT:
        break

    cv2.imshow("mywindow", img)
