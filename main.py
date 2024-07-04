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
                'Sky_condition': data['current']['condition']['text'],
                'icon': data['current']['condition']['icon']
            }
            return weather_info
        
    except:
        return 'Error', np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN

def create_table(cur):
    create_table_SQL = """
     CREATE TABLE IF NOT EXISTS student.de_vandy_current_weather (
      Location VARCHAR(50) PRIMARY KEY,
      temp_c FLOAT,
      humidity FLOAT,
      Wind_speed FLOAT,
      Feels_like FLOAT,
      Sky_condition VARCHAR(20),
      icon VARCHAR(255)
    )
    """
    cur.execute(create_table_SQL)
    conn.commit()
    

def upsert_data(conn, data):
    sql = f"""
    INSERT INTO student.de_vandy_current_weather (Location, temp_c, humidity, Wind_speed, Feels_like, Sky_condition, icon)
    VALUES ('{data['Location']}', {data['temp_c']}, {data['humidity']}, 
            {data['Wind_speed']}, {data['Feels_like']}, '{data['Sky_condition']}', '{data['icon']}')
    ON CONFLICT (Location) DO UPDATE SET
        temp_c = EXCLUDED.temp_c,
        humidity = EXCLUDED.humidity,
        Wind_speed = EXCLUDED.Wind_speed,
        Feels_like = EXCLUDED.Feels_like,
        Sky_condition = EXCLUDED.Sky_condition,
        icon = EXCLUDED.icon;
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
        upsert_data(conn, weather_details)

    cur.close()
    conn.close()
