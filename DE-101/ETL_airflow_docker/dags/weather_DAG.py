from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import requests
from config import url, API_KEY
import json
from datetime import datetime
import os

def extract_from_API() -> json:
    """
    Query openweathermap.com's API and to get the weather for
    Gomel, BY and then dump the json to the /src/data/ directory
    with the file name "<today's date>.json"
    """

    # My API key is defined in my config.py file.
    paramaters = {'q': 'Gomel, BY', 'appid': API_KEY}

    result = requests.get(url, paramaters)

    # If the API call was sucessful, get the json and dump it to a file with
    # today's date as the title.
    if result.status_code == 200:

        # Get the json data
        json_data = result.json()
        file_name = str(datetime.now().date()) + '.json'
        tot_name = os.path.join(os.path.dirname(__file__), 'data', file_name)

        with open(tot_name, 'w') as outputfile:
            json.dump(json_data, outputfile)
    else:
        print("Error In API call.")


def load_to_postgres(ds, **kwargs):
    """
    Processes the json data, checks the types and enters into the
    Postgres database.
    """

    pg_hook = PostgresHook(postgres_conn_id='postgres_connection')

    file_name = str(datetime.now().date()) + '.json'
    today_weather = os.path.join(os.path.dirname(__file__), 'data', file_name)

    # open the json datafile and read it in
    with open(today_weather, 'r') as inputfile:
        data = json.load(inputfile)

    city = str(data['name'])
    country = str(data['sys']['country'])
    latitude = float(data['coord']['lat'])
    longitude = float(data['coord']['lon'])
    humidity = float(data['main']['humidity'])
    pressure = float(data['main']['pressure'])
    temperature = float(data['main']['temp']) - 273.15
    weather = str(data['weather'][0]['description'])
    date = datetime.now().date()

    row = (city, country, latitude, longitude, humidity, pressure, temperature, weather, date)

    insert_data = """INSERT INTO weather_table
                (city, country, latitude, longitude,
                 humidity, pressure, temperature, weather, date)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""

    pg_hook.run(insert_data, parameters=row)


# Define the dag, the start date and how frequently it runs.
# I chose the dag to run everday by using 1440 minutes.
dag = DAG(
    dag_id='ETL_weather',
    start_date=datetime(2017, 8, 24),
    schedule_interval=timedelta(minutes=1440)
)

# First task is to query get the weather from openweathermap.org.
extract_data = PythonOperator(
    task_id='extract_data',
    provide_context=True,
    python_callable=extract_from_API,
    dag=dag)

# Second task is to process and load the data.

#Third task load data into the database.
load_data = PythonOperator(
    task_id='load_data',
    provide_context=True,
    python_callable=load_to_postgres,
    dag=dag)

# e = extract_from_API()
# t = process_data(e)
# l = load_to_postgres(t)
#
# # print(e)
# print(t)
# print(l)

extract_data >> load_data

if __name__ == "__main__":
    dag.cli()