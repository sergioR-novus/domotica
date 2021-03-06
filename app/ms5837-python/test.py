#!/usr/bin/python
import ms5837
import time
import requests


sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)
#sensor = ms5837.MS5837_30BA(0) # Specify I2C bus
#sensor = ms5837.MS5837_02BA()
#sensor = ms5837.MS5837_02BA(0)
#sensor = ms5837.MS5837(model=ms5837.MS5837_MODEL_30BA, bus=0) # Specify model and bus

currentstate = 0
previousstate = 0

# We must initialize the sensor before reading it
if not sensor.init():
        print("Sensor could not be initialized")
        exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    print("Sensor read failed!")
    exit(1)

print("Pressure: %.2f atm  %.2f Torr  %.2f psi") % (
sensor.pressure(ms5837.UNITS_atm),
sensor.pressure(ms5837.UNITS_Torr),
sensor.pressure(ms5837.UNITS_psi))

print("Temperature: %.2f C  %.2f F  %.2f K") % (
sensor.temperature(ms5837.UNITS_Centigrade),
sensor.temperature(ms5837.UNITS_Farenheit),
sensor.temperature(ms5837.UNITS_Kelvin))

freshwaterDepth = sensor.depth() # default is freshwater
sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
saltwaterDepth = sensor.depth() # No nead to read() again
sensor.setFluidDensity(1000) # kg/m^3
print("Depth: %.3f m (freshwater)  %.3f m (saltwater)") % (freshwaterDepth, saltwaterDepth)

# fluidDensity doesn't matter for altitude() (always MSL air density)
print("MSL Relative Altitude: %.2f m") % sensor.altitude() # relative to Mean Sea Level pressure in air

time.sleep(5)

# Spew readings
while True:
        if sensor.read():
                print("T: %0.2f C") % (sensor.temperature())
                #Logica y POST
                try:
                        print("BANDERA")

                        while True:
                                # Read  state
                                if sensor.read():
                                        print("T: %0.2f C") % (sensor.temperature())
                                else:
                                        print("Sensor read failed!")
                                        exit(1)

                                if sensor.temperature() > 30:
                                        currentstate = 1
                                else: 
                                        currentstate = 0
                                # If the bar is triggered
                                if currentstate == 1 and previousstate == 0:
                                
                                        print("Motion detected!")
                                        
                                        # Your IFTTT URL with event name, key and json parameters (values)
                                        r = requests.post('https://maker.ifttt.com/trigger/motion_detected/with/key/LN2n2aZaCLhO6u2IygYbV')
                                        #r = requests.post('https://maker.ifttt.com/trigger/motion_detected/with/key/LN2n2aZaCLhO6u2IygYbV', params={"value1":"none","value2":"none","value3":"none"})

                                        # Record new previous state
                                        previousstate = 1
                                        
                                        #Wait 120 seconds before looping again
                                        print("Waiting 120 seconds")
                                        time.sleep(120)
                                        
                                # If the PIR has returned to ready state
                                elif currentstate == 0 and previousstate == 1:
                                
                                        print("Ready")
                                        previousstate = 0

                                # Wait for 10 milliseconds
                                time.sleep(0.01)

                except KeyboardInterrupt:
                        print("    Quit")
                                
        else:
                print("Sensor read failed!")
                exit(1)


