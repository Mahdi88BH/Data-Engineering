import os
from dotenv import load_dotenv
import psycopg

load_dotenv()
password = os.getenv('passwordDB')


def load_data(df: object, postgre_table: object, postgre_schema: object) -> None:
    # Standardize column names to uppercase
    df.columns = [col.upper() for col in df.columns]
    
    # Strip any stray quotes or newlines from YAML schema definition
    clean_schema = postgre_schema.strip("'\" \n")
    insert_query = f"INSERT INTO {postgre_table} {clean_schema};"

    # Open a fresh connection context for this load operation
    with psycopg.connect(
        dbname="chicago_vehicle_crash_data",
        user="postgres",
        password=password,
        host="localhost"
    ) as conn:
        with conn.cursor() as cur:
            print("Successfully created the cursor object")

            for _, row in df.iterrows():
                if postgre_table == 'chicago_dmv.Crash':
                    insert_values = (
                        row.get('CRASH_UNIT_ID', None),
                        row.get('CRASH_ID', row.get('CRASH_RECORD_ID', None)),
                        row.get('PERSON_ID', None),
                        row.get('VEHICLE_ID', None),
                        row.get('NUM_UNITS', None),
                        row.get('TOTAL_INJURIES', row.get('INJURIES_TOTAL', None)),
                    )

                elif postgre_table == 'chicago_dmv.Vehicle':
                    insert_values = (
                        row.get('CRASH_UNIT_ID', None),
                        row.get('CRASH_ID', row.get('CRASH_RECORD_ID', None)),
                        row.get('CRASH_DATE', None),
                        row.get('VEHICLE_ID', None),
                        row.get('VEHICLE_MAKE', None),
                        row.get('VEHICLE_MODEL', None),
                        row.get('VEHICLE_YEAR', None),
                        row.get('VEHICLE_TYPE', None),
                    )

                elif postgre_table == 'chicago_dmv.Person':
                    insert_values = (
                        row.get('PERSON_ID', None),
                        row.get('CRASH_ID', row.get('CRASH_RECORD_ID', None)),
                        row.get('CRASH_DATE', None),
                        row.get('PERSON_TYPE', None),
                        row.get('VEHICLE_ID', None),
                        row.get('PERSON_SEX', None),
                        row.get('PERSON_AGE', None),
                    )

                else:
                    raise ValueError(f'Postgre Data Table {postgre_table} does not exist in this pipeline.')

                cur.execute(insert_query, insert_values)

            conn.commit()
            print(f"Successfully loaded and committed data into {postgre_table}")
    
    print('Successful closing of connection and cursor objects.')