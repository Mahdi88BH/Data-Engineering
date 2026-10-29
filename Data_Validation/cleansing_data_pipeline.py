import datetime as dt
from datetime import timedelta

import pandas as pd

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator


default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2026, 10, 29),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


def cleansing_data():
    df = pd.read_csv('/home/el7m7/Desktop/Data_Science/Data-Engineering/Data/scooter.csv')
    df.columns = [x.lower() for x in df.columns]
    df.drop('region_id', axis='columns')
    df['started_at'] = pd.to_datetime(df['started_at'], format='%m/%d/%Y %H:%M')

    df.to_csv('/home/el7m7/Desktop/Data_Science/Data-Engineering/Data/cleaning_dataset_scooter.csv', index=False)


def filtered_data():
    df = pd.read_csv('/home/el7m7/Desktop/Data_Science/Data-Engineering/Data/cleaning_dataset_scooter.csv')

    fromd = '2019-05-23'
    tod='2019-06-03'
    tofrom = df[(df['started_at'] > fromd) & (df['started_at'] < tod)]

    tofrom.to_csv('/home/el7m7/Desktop/Data_Science/Data-Engineering/Data/may23-june3.csv')



with DAG(
    'CleanData',
    default_args=default_args,
     schedule=timedelta(minutes=5)
) as dag:


    clean_data = PythonOperator(
        task_id='LoadandTronsformData',
        python_callable=cleansing_data
    )


    extract_data = PythonOperator(
        task_id='ExtractSubSetFromData',
        python_callable=filtered_data
    )


    copy_file = BashOperator(
        task_id='CopyFileToHomeDirectory',
        bash_command='cp /home/el7m7/Desktop/Data_Science/Data-Engineering/Data/may23-june3.csv /home/el7m7/Desktop/'
    )


    clean_data >> extract_data >> copy_file