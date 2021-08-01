import RPi.GPIO as GPIO
import time
import requests
from w1thermsensor import W1ThermSensor
from ISStreamer.Streamer import Streamer

sensor = W1ThermSensor()
pinpir = 17
GPIO.setup(pinpir, GPIO.IN)
currentstate = 0
previousstate = 0


# --------- User Settings ---------
SENSOR_LOCATION_NAME = "Casa"
BUCKET_NAME = ":partly_sunny: Room stats"
BUCKET_KEY = "test"
ACCESS_KEY = "ist_ENpoPBXw1ubY9eAaNld52lkMMLpjKAgS"
MINUTES_BETWEEN_READS = .05
# ---------------------------------

streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)


while True:
        try:
                temp_c = sensor.get_temperature()
                streamer.log(SENSOR_LOCATION_NAME + " Temperature(C)", temp_c)
                print(temp_c)  
                print("Waiting for PIR to settle ...")
                while GPIO.input(pinpir) == 1:
                        currentstate = 0
                        print(GPIO.input(pinpir))
                        time.sleep(1)
                print("    Ready")
                currentstate = GPIO.input(pinpir)
                if currentstate == 1 and previousstate == 0:
                        streamer.log(SENSOR_LOCATION_NAME + " Movimiento", True)
                        print("Motion detected!")
                        r = requests.post('https://maker.ifttt.com/trigger/motion_detected/with/key/LN2n2aZaCLhO6u2IygYbV', params={"value1":"none","value2":"none","value3":"none"})
                        previousstate = 1
                        print("Waiting 10 seconds")
                        time.sleep(10)
                elif currentstate == 0 and previousstate == 1:
                        print("Ready")
                        previousstate = 0
                        time.sleep(0.01)
                streamer.flush()
                time.sleep(60*MINUTES_BETWEEN_READS)

   
        except RuntimeError:
                print("RuntimeError, trying again...")
                print("    Quit")
	        # GPIO.cleanup()
                continue