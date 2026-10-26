import datetime as dt
from datetime import timedelta

import pandas as pd
from airflow import DAG

# Mandatory for Airflow 3.x standard operators
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator


def csv_to_json():
  csv_path = "/home/el7m7/Desktop/Data_Science/Data-Engineering/Data/data.csv"
  json_path = "/home/el7m7/Desktop/Data_Science/Data-Engineering/Data/AirFlow_data.json"

  df = pd.read_csv(csv_path)
  for i, r in df.iterrows():
    print(r["name"])
  df.to_json(json_path, orient="records")


default_args = {
    "owner": "airflow",
    "start_date": dt.datetime(2026, 10, 26),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "MYCSVDAG",
    default_args=default_args,
    schedule=timedelta(minutes=5),
    catchup=False,
) as dag:
  print_starting = BashOperator(
      task_id="starting",
      bash_command='echo "I am reading the CSV now ....."',
  )

  csv_json = PythonOperator(
      task_id="convert_csv_To_json", python_callable=csv_to_json
  )

  print_starting >> csv_json