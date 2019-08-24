from imutils import build_montages
import numpy as np
import imagezmq
import imutils
import cv2

imageHub = imagezmq.ImageHub()

while True:
    (rpiName, frame) = imageHub.recv_image()
    imageHub.send_reply(b'OK')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 1)
    edged = cv2.Canny(blurred, 40, 40)
    shape = (frame.shape[1]*2, frame.shape[0]*2)
    cv2.imshow("Raw", frame)
    cv2.imshow("Blurred", blurred)
    cv2.imshow("Edged", cv2.resize(edged, shape))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break