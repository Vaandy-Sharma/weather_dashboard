import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
import psycopg2 as psql
import os
from dotenv import load_dotenv

st.set_page_config(layout="wide")

# Fetching data from the database
def fetch_data():
    load_dotenv()
    password = os.getenv('SQLPass')
    user = os.getenv('SQLUser')
    my_host = os.getenv('host')

    conn = psql.connect(
        database='pagila',
        user=user,
        host=my_host,
        password=password,
        port=5432
    )
    query = "SELECT * FROM student.de_vandy_current_weather"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = fetch_data()

nowTime = datetime.now()
current_time = nowTime.strftime("%H:%M:%S")
today = str(date.today())

# Setting current location to London
london_data = df[df['location'] == 'London']

def create_css_style(title, value, is_image=False):
    if is_image:
        
        return f"""
            <div style="background-color: grey; padding: 10px; border-radius: 5px; margin-bottom: 0px; margin-top: 0px">
                <p style="color: white; font-size: 25px; font-weight: 700;">{title}</p>
                <img src="{value}" alt="{title}" style="width: 150px; height: 150px;">
            </div>
        """
    else:
        return f"""
            <div style="background-color: grey; padding: 10px; border-radius: 5px; margin-bottom: 0px; margin-top: 0px">
                <p style="color: white; font-size: 25px; font-weight: 700;">{title}</p>
                <h3 style="color: white; font-size: 40px; font-weight: 700;">{value}</h3>
            </div>
        """

# Add title and weather icon
icon_url = 'http:' + london_data.iloc[0]['icon'] if london_data.iloc[0]['icon'].startswith('//') else london_data.iloc[0]['icon']
st.markdown(f"""
    <div style="display: flex; align-items: center;">
        <h1 style="margin-right: 20px;">Current Weather Forecast</h1>
        <img src="{icon_url}" alt="Weather Icon" style="width: 100px; height: 100px;">
    </div>
    """, unsafe_allow_html=True)

# Row A
st.markdown('<div class="row-container">', unsafe_allow_html=True)
a1, a2, a3 = st.columns(3)
with a1:
    st.markdown(create_css_style("Date", today), unsafe_allow_html=True)
with a2:
    st.markdown(create_css_style("Location", london_data.iloc[0]['location']), unsafe_allow_html=True)
with a3:
    st.markdown(create_css_style("Time", current_time), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Row B
st.markdown('<div class="row-container">', unsafe_allow_html=True)
b1, b2, b3, b4 = st.columns(4)
with b1:
    st.markdown(create_css_style("Temperature (°C)", london_data.iloc[0]['temp_c']), unsafe_allow_html=True)
with b2:
    st.markdown(create_css_style("Feels Like (°C)", london_data.iloc[0]['feels_like']), unsafe_allow_html=True)
with b3:
    st.markdown(create_css_style("Sky Condition", london_data.iloc[0]['sky_condition']), unsafe_allow_html=True)
with b4:
    st.markdown(create_css_style("Humidity (%)", london_data.iloc[0]['humidity']), unsafe_allow_html=True)


st.header("Comparison with Other Cities")

# Create columns for the charts
chart_col1, chart_col2, chart_col3 = st.columns(3)

# Line chart comparing Temperature and Feels Like
with chart_col1:
    fig, ax = plt.subplots(figsize=(5, 3))  
    
    ax.plot(df['location'], df['temp_c'], label='Temperature', color='#FF6347', marker='o')
    ax.plot(df['location'], df['feels_like'], label='Feels Like', color='#4682B4', marker='o')
    
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_xlabel('Location')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Temperature comparison')
    ax.legend()
    st.pyplot(fig)

# Line chart for Temperature
with chart_col2:
    fig_temp, ax_temp = plt.subplots(figsize=(5, 3))  
    ax_temp.plot(df['location'], df['temp_c'], marker='o', linestyle='-', color='#FF6347', label='Temperature (°C)')
    
    ax_temp.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax_temp.set_xlabel('Location')
    ax_temp.set_ylabel('Temperature (°C)')
    ax_temp.set_title('Temperature by City')
    ax_temp.legend()
    st.pyplot(fig_temp)

# Line chart for Humidity
with chart_col3:
    fig_hum, ax_hum = plt.subplots(figsize=(5, 3))  
    ax_hum.plot(df['location'], df['humidity'], marker='o', linestyle='-', color='#4682B4', label='Humidity (%)')
    
    ax_hum.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax_hum.set_xlabel('Location')
    ax_hum.set_ylabel('Humidity (%)')
    ax_hum.set_title('Humidity by City')
    ax_hum.legend()
    st.pyplot(fig_hum)
