import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO
import time

# define pins for sensors
DHT_PIN = 4
BMP_SDA = 3
BMP_SCL = 5

# create sensors objects
dht_sensor = Adafruit_DHT.DHT11
bmp_sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

# define function to read sensor data
def read_sensor_data():
    # read temperature and humidity
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, DHT_PIN)

    # read pressure
    pressure = bmp_sensor.read_pressure()

    return {'temperature': temperature, 'humidity': humidity, 'pressure': pressure}

# loop to continuously read sensor data
while True:
    data = read_sensor_data()
    # insert data into database
    # wait for some time (e.g. 5 minutes)
    time.sleep(300)