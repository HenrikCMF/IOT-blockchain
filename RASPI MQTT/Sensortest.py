import board
import busio

import adafruit_ads1x15.ads1115 as ADS
import bme680
from adafruit_ads1x15.analog_in import AnalogIn
import time
i2c=busio.I2C(board.SCL, board.SDA)

ads=ADS.ADS1115(i2c)
ads.gain=2/3
chan=AnalogIn(ads, ADS.P0)

a=-42.24
b=184

#while 1:
    #hum, tem = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    #print(hum)
time.sleep(1)

chan=AnalogIn(ads, ADS.P0)

print(a*chan.voltage+b)

bmesensor=bme680.BME680(bme680.I2C_ADDR_SECONDARY)

for name in dir(bmesensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(bmesensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))
print('\n\nInitial reading:')
for name in dir(bmesensor.data):
    value = getattr(bmesensor.data, name)

    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

while 1:
    if bmesensor.get_sensor_data():
        print(bmesensor.data.temperature)
