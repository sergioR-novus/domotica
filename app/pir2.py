import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)         #Read output from PIR motion sensor
while True:
    i=GPIO.input(4)
    print(i)
    time.sleep(1)
    if i==0:                 #When output from motion sensor is LOW
        print "No intruders",i
        time.sleep(0.1)
    elif i==1:               #When output from motion sensor is HIGH
        print "Intruder detected",i
        time.sleep(0.1)