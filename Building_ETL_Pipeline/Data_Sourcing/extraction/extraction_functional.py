import os
from io import StringIO
import urllib3
import certifi
import json
import sqlite3
import pandas as pd

import logging


logger = logging.getLogger()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_data_from_csv(path_csv: str) -> pd.DataFrame:
    """
        Extract data from a CSV file.
        
        Args:
            file_path (str): Path to the CSV file.
    """

    try:
        df_csv = pd.read_csv(path_csv)
        logger.info(f"Successfully loaded the CSV file from {path_csv} with {df_csv.shape[0]} records")
    except Exception as e:
        logger.exception(f"Failed to load Data From CSV file in {path_csv} Error: {e}")
        df_csv = pd.DataFrame()

    return df_csv



def extract_data_from_parquet(path_parquet: str) -> pd.DataFrame:
    """
    Extract data from a Parquet file.
    
    Args:
        file_path (str): Path to the Parquet file.
    """

    try:
        df_parquet = pd.read_parquet(path_parquet)
        logger.info(f"Successfully loaded the Parquet file from {path_parquet} with {df_parquet.shape[0]} records")
    except Exception as e:
        logger.exception(f"Failed to load Data From Parquet file in {path_parquet} Error: {e}")
        df_parquet = pd.DataFrame()

    return df_parquet



def extract_data_from_database(path_db: str) -> pd.DataFrame:
    """
        Extract data from a database sqlite .
        
        Args:
            file_db (str): Path to the sqlite db.
    """

    try:
        with sqlite3.connect(path_db) as conn:
            df_db = pd.read_sql("SELECT * FROM movies", conn)
    except Exception as e:
        logger.exception(f"Failde to load data from database sqlite error : {e}")
        df_db = pd.DataFrame()

    return df_db


def extract_data_from_api(api_endpoint: str) -> pd.DataFrame:
    """
        Extract data from a API .
        
        Args:
            api_endpoint (str): url to the endpoint.
    """

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    try:
        response = http.request('GET', api_endpoint, timeout=10.0)
        print(f"Status Code : {response.status}")

        if response.status == 200:
            data = json.loads(response.data.decode('utf-8'))
            df_api = pd.json_normalize(data)
            logger.info(f"Seccessfully loaded data from api with {df_api.shape[0]}")

        else:
            print(f"Server Error : {response.status}")
            df_api = pd.DataFrame()
    except Exception as e:
        logger.exception(f"Failed to extract Data error : {e}")
        df_api = pd.DataFrame()

    return df_api



def extract_data_from_web_page(url: str, matching_word: str) -> pd.DataFrame:
    """
        Extract data from page Web .
            
        Args:
            url (str): url to the page Web.
    """

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:

        res = urllib3.request('GET', url, headers=headers)

        if res.status == 200:
            data = res.data.decode('utf-8')
            df_html = pd.read_html(StringIO(data), match=matching_word)
            logger.info(f'Successfully loaded! Found {len(df_html)} table(s).')
        else:
            print(f"Failed to load data from {url}")
            df_html = pd.DataFrame()
    except Exception as e:
        logger.exception(f"Failure to load Data - Error : {e}")
        df_html = pd.DataFrame()

    return df_html


def extract_all_data():
    path_csv = '~/Desktop/Data_Science/Data-Engineering/Building_ETL_Pipeline/Data_Sourcing/Data/h9gi-nx95.csv'
    path_parquet = '~/Desktop/Data_Science/Data-Engineering/Building_ETL_Pipeline/Data_Sourcing/Data/yellow_tripdata_2022-01.parquet'
    path_db = '~/Desktop/Data_Science/Data-Engineering/Building_ETL_Pipeline/Data_Sourcing/Data/movies.sqlite'
    api_endpoint = 'https://data.cityofnewyork.us/resource/h9gi-nx95.json?$limit=500'
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
    matching_word = 'by country'


    df_csv, df_parquet, df_db, df_api, df_html = (extract_data_from_csv(path_csv),
                                                  extract_data_from_parquet(path_parquet),
                                                  extract_data_from_database(path_db),
                                                  extract_data_from_api(api_endpoint),
                                                  extract_data_from_web_page(url, matching_word)
    )

    return df_csv, df_parquet, df_db, df_api, df_html
    

