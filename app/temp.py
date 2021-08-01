import time
from w1thermsensor import W1ThermSensor
from ISStreamer.Streamer import Streamer
sensor = W1ThermSensor()


# --------- User Settings ---------
SENSOR_LOCATION_NAME = "Casa"
BUCKET_NAME = ":partly_sunny: Room Temperatures"
BUCKET_KEY = "dht22sensor"
ACCESS_KEY = "ist_ENpoPBXw1ubY9eAaNld52lkMMLpjKAgS"
MINUTES_BETWEEN_READS = .05
METRIC_UNITS = True
# ---------------------------------

streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

while True:

    try:
        temp_c = sensor.get_temperature()
        print("The temperature is %s celsius" % temp_c)
    

    if METRIC_UNITS:
        streamer.log(SENSOR_LOCATION_NAME + " Temperature(C)", temp_c)

    else:
        temp_f = format(temp_c * 9.0 / 5.0 + 32.0, ".2f")
        streamer.log(SENSOR_LOCATION_NAME + " Temperature(F)", temp_f)

    streamer.flush()
    time.sleep(60*MINUTES_BETWEEN_READS)