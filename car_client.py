from imutils.video import VideoStream
import imagezmq
import socket
import time
import cv2

def prepServo(angle=40, pin=16):
    import RPi.GPIO as GPIO
    from time import sleep
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    servo = GPIO.PWM(16, 50)
    servo.start(0)
    duty = angle / 18 + 2
    GPIO.output(pin, True)
    servo.ChangeDutyCycle(duty)
    sleep(0.3)
    GPIO.output(pin, False)
    servo.ChangeDutyCycle(0)



prepServo()
time.sleep(1)
my_server = '192.168.178.78'
sender = imagezmq.ImageSender(connect_to="tcp://192.168.178.78:5555")

rpiName = socket.gethostname()
vs = VideoStream(usePiCamera=True, resolution=(200, 160), framerate=20).start()

time.sleep(1)
 
while True:
    frame = vs.read()
    sender.send_image(rpiName, frame)
    