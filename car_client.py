import io
import socket
import struct
import time
import picamera
import sys
from time import sleep

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

class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; send the old one's length
            # then the data
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)

prepServo()
sleep(1)
my_server = '192.168.178.78'
res = (1280, 720)
client_socket = socket.socket()
client_socket.connect((my_server, 8000))
connection = client_socket.makefile('wb')
try:
    output = SplitFrames(connection)
    with picamera.PiCamera(resolution=res, framerate=30) as camera:
        time.sleep(2)
        start = time.time()
        camera.start_recording(output, format='mjpeg')
        camera.wait_recording(9999)
        camera.stop_recording()
        # Write the terminating 0-length to the connection to let the
        # server know we're done
        connection.write(struct.pack('<L', 0))
finally:
    finish = time.time()
    print('Sent %d images in %d seconds at %.2ffps' % (
    output.count, finish-start, output.count / (finish-start)))
    connection.close()
    client_socket.close()