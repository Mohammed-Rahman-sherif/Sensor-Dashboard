import psycopg2
from datetime import datetime
import pytz
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

# define database connection details
conn = psycopg2.connect(database="postgres", user="postgres", password="MASHAALLAH", host="localhost", port="5432")
cur = conn.cursor()

# define function to insert data into database
def insert_data(data):
    try:
        # execute SQL query to create table if not exists and insert data
        create_table_query = "CREATE TABLE IF NOT EXISTS sensor_data_latest (temperature INT, humidity INT, pressure INT, created_at TIMESTAMP);"
        cur.execute(create_table_query)
        insert_data_query = "INSERT INTO sensor_data_latest (temperature, humidity, pressure, created_at) VALUES (%s, %s, %s, %s);"
        current_time_utc = datetime.utcnow()
        utc_timezone = pytz.timezone('UTC')
        current_time_utc = utc_timezone.localize(current_time_utc)
        ist_timezone = pytz.timezone('Asia/Kolkata')
        current_time_ist = current_time_utc.astimezone(ist_timezone)
        current_time_str = current_time_ist.strftime("%Y-%m-%d %I:%M:%S.%f %p")[:-3]
        cur.execute(insert_data_query, (data['temperature'], data['humidity'], data['pressure'], current_time_str))
        # commit the transaction
        conn.commit()
        print("Data has been inserted successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error inserting data:", error)

# loop to continuously read sensor data and insert into database
while True:
    data = read_sensor_data()
    insert_data(data)
    # wait for some time (e.g. 5 minutes)
    time.sleep(300)
