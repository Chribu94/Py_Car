from imutils import build_montages
import numpy as np
import imagezmq
import imutils
import cv2

imageHub = imagezmq.ImageHub()

while True:
    (rpiName, frame) = imageHub.recv_image()
    imageHub.send_reply(b'OK')
    cv2.imshow("Raw", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break