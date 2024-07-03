from dotenv import load_dotenv
import requests
import psycopg2 as psql
import os
import pandas as pd
import numpy as np

def get_details(city, api_key):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                'Location': data['location']['name'],
                'temp_c': data['current']['temp_c'],
                'humidity': data['current']['humidity'],
                'Wind_speed': data['current']['wind_mph'],
                'Feels_like': data['current']['feelslike_c'],
                'Sky_condition': data['current']['condition']['text']
            }
            return weather_info
        
    except:
        return 'Error', np.NAN, np.NAN, np.NAN, np.NAN, np.NAN , np.NAN

def create_table(cur):
    create_table_SQL= """
    CREATE TABLE IF NOT EXISTS student.de_vandy_current_weather (
      row_id SERIAL PRIMARY KEY,
      Location VARCHAR(50),
      temp_c FLOAT,
      humidity FLOAT,
      Wind_speed FLOAT,
      Feels_like FLOAT,
      Sky_condition VARCHAR(20)
    )
    """
    cur.execute(create_table_SQL)
    conn.commit()
    

def insert_data(conn, data):
    sql = f"""
    INSERT INTO student.de_vandy_current_weather (Location, temp_c, humidity, Wind_speed, Feels_like, Sky_condition)
    VALUES ('{data['Location']}', {data['temp_c']}, {data['humidity']}, 
            {data['Wind_speed']}, {data['Feels_like']}, '{data['Sky_condition']}')
    """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    
if __name__ == "__main__":
    

    
    load_dotenv()
    api_key = os.getenv('API_KEY')
    password = os.getenv('SQLPass')
    user = os.getenv('SQLUser')
    my_host = os.getenv('host')

    
    location = ["London", "Paris", "New York", "New Delhi"]

    
    conn = psql.connect(
        database='pagila',
        user=user,
        host=my_host,
        password=password,
        port=5432
    )
    cur = conn.cursor()

    
    create_table(cur)

    
    for city in location:
        weather_details = get_details(city, api_key)
        insert_data(conn, weather_details)
    
    cur.close()
    conn.close()
    
