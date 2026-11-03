import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import psycopg2 as db



default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2026, 10, 28),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def query_postgresql():

    conn_string = "dbname='dataengineering' host='localhost' user='postgres' password='Postgres_@8899'"
    conn = db.connect(conn_string)

    if conn.closed == 0:
        print("Connection to PostgreSQL datbase is successfuly established")

        query = "select * from users"
        df = pd.read_sql(query, con=conn)
        df.columns = ['name', 'id', 'street', 'city', 'zip']

        df.to_csv('/home/el7m7/Desktop/Data_Science/Data-Engineering/Data/quering_data_from_postgresql_db.csv', index=False)
        print("The Data has saved successfuly")
    else:
         print("Connection failure")


def insert_data_to_elasticsearch():

    df = pd.read_csv('/home/el7m7/Desktop/Data_Science/Data-Engineering/Data/quering_data_from_postgresql_db.csv')
    
    es = Elasticsearch(
        'https://localhost:9200',
        basic_auth=('elastic', 'Elastic_@8899'),
        verify_certs=False
    )

    actions = [
        {
            '_index': 'new_users',
            '_source': {
                'name': row['name'],
                'id': row['id'],
                'street': row['street'],
                'city': row['city'],
                'zip': row['zip']
            }
        }
        for _, row in df.iterrows()
    ]

    success_count, error = helpers.bulk(es, actions)

    print(f"Successful indexed : {success_count} document")
    if error:
        print(f"Errors Encountred : {error}")



with DAG(
    'MyDBdag',
    default_args=default_args,
    schedule=timedelta(minutes=5),
) as dag:
    
    get_data = PythonOperator(
        task_id='QueryPostgreSQL',
        python_callable=query_postgresql
    )

    insert_data = PythonOperator(
        task_id='InsertDataToElasticSearch',
        python_callable=insert_data_to_elasticsearch
    )


get_data >> insert_data