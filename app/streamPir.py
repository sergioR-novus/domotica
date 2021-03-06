#! /usr/bin/python

# Imports
import RPi.GPIO as GPIO
import time
import requests
from ISStreamer.Streamer import Streamer

# --------- User Settings ---------
SENSOR_LOCATION_NAME = "Casa"
BUCKET_NAME = ":partly_sunny: Room stats"
BUCKET_KEY = "pir"
ACCESS_KEY = "ist_ENpoPBXw1ubY9eAaNld52lkMMLpjKAgS"
MINUTES_BETWEEN_READS = .05
METRIC_UNITS = True
# ---------------------------------

streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)


print(time.strftime("%H:%M:%S", time.localtime()))


# Set the GPIO naming convention
GPIO.setmode(GPIO.BCM)

# Turn off GPIO warnings
GPIO.setwarnings(False)

# Set a variable to hold the GPIO Pin identity
pinpir = 17

# Set GPIO pin as input
GPIO.setup(pinpir, GPIO.IN)

# Variables to hold the current and last states
currentstate = 0
previousstate = 0

try:
	print("Waiting for PIR to settle ...")
	
	# Loop until PIR output is 0
	while GPIO.input(pinpir) == 1:
            currentstate = 0
            print(GPIO.input(pinpir))
            time.sleep(1)

	print("    Ready")
	# Loop until users quits with CTRL-C
	while True:
		# Read PIR state
		currentstate = GPIO.input(pinpir)
		# If the PIR is triggered
		if currentstate == 1 and previousstate == 0:
                    streamer.log(SENSOR_LOCATION_NAME + " Movimiento", True)
                    print("Motion detected!")
                    # Your IFTTT URL with event name, key and json parameters (values)
                    r = requests.post('https://maker.ifttt.com/trigger/motion_detected/with/key/LN2n2aZaCLhO6u2IygYbV', params={"value1":"none","value2":"none","value3":"none"})
                    # Record new previous state
                    previousstate = 1
                    #Wait 120 seconds before looping again
                    print("Waiting 10 seconds")
                    time.sleep(10)
		# If the PIR has returned to ready state
		elif currentstate == 0 and previousstate == 1:
                    print("Ready")
                    previousstate = 0
                # Wait for 10 milliseconds
                    time.sleep(0.01)
                    streamer.flush()
                    time.sleep(60*MINUTES_BETWEEN_READS)
except KeyboardInterrupt:
	print("    Quit")
	# Reset GPIO settings
	GPIO.cleanup()