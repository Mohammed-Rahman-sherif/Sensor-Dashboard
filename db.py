import psycopg2
from datetime import datetime
import pytz

data = {'temperature': 5, 'humidity': 10, 'pressure': 10}

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


# call the insert_data function to insert data into database
insert_data(data)
