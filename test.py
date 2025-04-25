import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv(override=True)

"""Fetches activity records from the PostgreSQL database."""
# PostgreSQL connection details
DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}



def test():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
                SELECT date, time, activity_type, finish_time, note FROM main ORDER BY date DESC;
            """)

            # Fetch all records from the query
    records = cursor.fetchall()
    print(records)



test()