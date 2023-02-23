import requests
from config import url, API_KEY
import json
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook


def extract_data() -> json:
    """
    Query openweathermap.com's API and to get the weather for
    Brooklyn, NY in json"
    """

    # My API key is defined in my config.py file.
    paramaters = {'q': 'Gomel, BY', 'appid': API_KEY}
    result = requests.get(url, paramaters)

    if result.status_code == 200:
        json_data = result.json()
        return json_data
    else:
        print("Error In API call.")


def transform_data() -> tuple:
    """
    Make some data transformation
    """

    data = extract_data()

    city = str(data['name'])
    country = str(data['sys']['country'])
    lat = float(data['coord']['lat'])
    lon = float(data['coord']['lon'])
    humid = float(data['main']['humidity'])
    press = float(data['main']['pressure'])
    temp = float(data['main']['temp']) - 273.15
    weather = str(data['weather'][0]['description'])
    date = datetime.now().date()

    row = (city, country, lat, lon, humid, press, temp, weather, date)

    return row


def load_data():
    """
    Processes the json data, checks the types and enters into the
    Postgres database.
    """
    row = transform_data()

    pg_hook = PostgresHook(postgres_conn_id='postgres_connection')

    insert_data = """INSERT INTO weather_table
                 (city, country, latitude, longitude,
                 humidity, pressure, temperature, weather, date)
                 VALUES
                 (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    pg_hook.run(insert_data, parameters=row)
