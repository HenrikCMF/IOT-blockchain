import board
import busio

import adafruit_ads1x15.ads1115 as ADS
import bme680
from adafruit_ads1x15.analog_in import AnalogIn
import time

i2c=None
ads=None
bmesensor=None

a=-42.24
b=184

def init_sensors():
    global ads
    global i2c
    global bmesensor
    i2c=busio.I2C(board.SCL, board.SDA)
    ads=ADS.ADS1115(i2c)
    ads.gain=2/3
    chan=AnalogIn(ads, ADS.P0)
    
    bmesensor=bme680.BME680(bme680.I2C_ADDR_SECONDARY)
    for name in dir(bmesensor.calibration_data):
        if not name.startswith('_'):
            value = getattr(bmesensor.calibration_data, name)
    for name in dir(bmesensor.data):
        value = getattr(bmesensor.data, name)

def read_humidity():
    chan=AnalogIn(ads, ADS.P0)
    return chan.voltage
    
def read_temperature():
    if bmesensor.get_sensor_data():
        return bmesensor.data.temperature
