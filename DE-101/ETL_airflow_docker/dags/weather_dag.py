from datetime import timedelta
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow import DAG
from tasks import extract_data, transform_data, load_data


# Define the dag, the start date and how frequently it runs.
# I chose the dag to run everyay by using 1440 minutes.
dag = DAG(
    dag_id='ETL_weather',
    start_date=datetime(2017, 8, 24),
    schedule_interval=timedelta(minutes=1440)
)

# First task is to query get the weather from openweathermap.org.
extract = PythonOperator(
    task_id='extract',
    provide_context=True,
    python_callable=extract_data,
    dag=dag)

# Second task is to process the data.
transform = PythonOperator(
    task_id='transform',
    provide_context=True,
    python_callable=transform_data,
    dag=dag)

#Third task load data into the database.
load = PythonOperator(
    task_id='load',
    provide_context=True,
    python_callable=load_data,
    dag=dag)


extract >> transform >> load

if __name__ == "__main__":
    dag.cli()