from fastapi import FastAPI, Request, responses
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List
import psycopg2

app = FastAPI()

# Define database connection details
conn = psycopg2.connect(database="postgres", user="postgres", password="MASHAALLAH", host="localhost", port="5432")
cur = conn.cursor()

def get_sensor_data():
    try:
        # Execute SQL query to retrieve latest data
        query = "SELECT * FROM sensor_data_latest ORDER BY created_at DESC"
        cur.execute(query)
        rows = cur.fetchall()
        # Return the data as a list of dictionaries
        data = []
        for row in rows:
            data.append({
                'temperature': row[0],
                'humidity': row[1],
                'pressure': row[2],
                'created_at': row[3].strftime('%Y-%m-%d %H:%M:%S')
            })
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error retrieving sensor data from database:", error)


# Define API endpoint to retrieve sensor data
@app.get("/sensor-data", response_class=HTMLResponse)
async def read_sensor_data(request: Request):
    # Retrieve data from database
    data = get_sensor_data()
    # Check if data exists
    if data:
        return templates.TemplateResponse("index.html", {"request": request, "data": data})
    else:
        return responses.JSONResponse(content={"message": "Error retrieving sensor data from database"}, status_code=404)

# Define templates directory
templates = Jinja2Templates(directory="template")
