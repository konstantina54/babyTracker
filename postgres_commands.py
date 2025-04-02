import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

def fetch_activity_data():
    """Fetches activity records from the PostgreSQL database."""
    # PostgreSQL connection details
    DB_CONFIG = {
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT")
    }
    print(os.environ['DB_PASSWORD'])
    # Mapping activity_type ID to readable activity names
    ACTIVITY_MAP = {
        1: "Food",
        2: "Sleep",
        3: "Potty"
    }

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # SQL query to retrieve relevant data
        cursor.execute("""
            SELECT date, time, activity_type, note FROM main ORDER BY date DESC;
        """)

        # Fetch all records from the query
        records = cursor.fetchall()

        # Convert list of tuples into Pandas DataFrame
        df = pd.DataFrame(records, columns=['Date', 'Start Time', 'Activity Type', 'Note'])

        # Convert activity type IDs to readable names
        df['Activity Type'] = df['Activity Type'].map(ACTIVITY_MAP)

        return df  

    except psycopg2.Error as e:
        print("Database error:", e)
        return pd.DataFrame(columns=['Date', 'Start Time', 'Activity Type', 'Note'])  # Return empty DataFrame on error

    finally:
        # Ensure cleanup of database resources
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
