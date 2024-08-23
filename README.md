# Live Weather Dashboard

This project is a **Live Weather Dashboard** that tracks and displays real-time weather data for **London** and other major cities using a public weather API. The dashboard is built to provide an intuitive, visually appealing interface for users to easily monitor key weather parameters, such as **temperature**, **humidity**, and the **"feels like" temperature**, all updated every 15 minutes.

## Features

- **Real-time Weather Tracking**: The application continuously tracks real-time weather data for multiple cities including London, updating every 15 minutes.
  
- **Data Visualization**: Python scripts combined with **Streamlit** are used to create an interactive, easy-to-use dashboard to visualize weather data trends. Users can compare different weather variables across cities.

- **ETL Pipeline**: A custom-built **ETL (Extract, Transform, Load)** pipeline automatically processes the data. 
  - **Extract**: The data is pulled from the weather API at regular intervals.
  - **Transform**: Data is cleaned and transformed for analysis.
  - **Load**: Transformed data is loaded into a **PostgreSQL** database for persistent storage and future analysis.

- **Automated Data Updates**: Using **cron jobs**, the ETL pipeline runs every 15 minutes to fetch the latest weather data and ensure the dashboard displays up-to-date information.

- **City Comparisons**: The dashboard allows for comparisons between cities, showing variations in temperature, humidity, and "feels like" temperature in real time.

## Technology Stack

### Backend:
- **Weather API**: Fetches live weather data for cities like London and other major cities.
- **ETL Pipeline**: Developed using **Python** to automate data extraction, transformation, and loading into a PostgreSQL database.
- **PostgreSQL**: Stores the weather data collected over time for persistent access.

### Frontend:
- **Streamlit**: An interactive, web-based framework used to display the live dashboard with graphs and visual comparisons of weather data.
  
### Scheduling:
- **Cron Jobs**: Used to schedule the ETL pipeline to run every 15 minutes, ensuring the data is regularly updated without manual intervention.

## Project Workflow

1. **Data Extraction**: 
   - The weather data is extracted from the public API at 15-minute intervals.
   
2. **Data Transformation**:
   - Data is cleaned and transformed, ensuring proper format for analysis (e.g., temperature conversions, date formatting).

3. **Data Loading**:
   - Transformed data is loaded into a **PostgreSQL** database for storage.

4. **Visualization**:
   - Data is visualized on a **Streamlit** dashboard, allowing users to monitor weather data in real-time and compare weather parameters across cities.

## Setup and Installation

### Prerequisites:
- **Python 3.x**
- **PostgreSQL**
- Weather API access key (e.g., from OpenWeatherMap)
  
### Installation:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/weather-dashboard.git
   cd weather-dashboard
