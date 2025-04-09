import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

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
            SELECT date, time, activity_type, finish_time, note FROM main ORDER BY date DESC;
        """)

        # Fetch all records from the query
        records = cursor.fetchall()

        # Convert list of tuples into Pandas DataFrame
        df = pd.DataFrame(records, columns=['Date', 'Start Time', 'Activity Type','Finish Time', 'Note'])

        # Convert activity type IDs to readable names
        df['Activity Type'] = df['Activity Type'].map(ACTIVITY_MAP)
        # Only update notes for Sleep activities
        sleep_mask = (df['Activity Type'] == "Sleep") & (df['Finish Time'].notna()) & (df['Start Time'].notna())

        df.loc[sleep_mask, 'Note'] = df[sleep_mask].apply(
            lambda row: calculate_duration(row['Start Time'], row['Finish Time']),
            axis=1
        )

        # Drop Finish Time column
        df.drop(columns=['Finish Time'], inplace=True)
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




def calculate_duration(start_time_obj, finish_time_obj):
    """Calculate time difference in hours and minutes between two datetime.time objects."""
    try:
        today = datetime.today().date()
        start_dt = datetime.combine(today, start_time_obj)
        finish_dt = datetime.combine(today, finish_time_obj)

        # Handle overnight case
        if finish_dt < start_dt:
            finish_dt += timedelta(days=1)

        duration = finish_dt - start_dt
        total_minutes = int(duration.total_seconds() // 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours}h {minutes}m"
    except Exception as e:
        return f"Error: {e}"



def sql_new_entry(activity, input_type, date, start_time, finish_time = None, note = None):
    # establishing the connection
    print(activity, input_type, date, start_time, finish_time, note)
    DB_CONFIG = {
        "database":"baby_tracker",
        'user':'postgres',
        'password':'Learner1',
        'host':'localhost',
        'port':'5432'
    }

    ACTIVITY_MAP = {
    "food": 1,   # food
    "sTime": 2,  # sleep
    "potty": 3   # potty
    }

    activity_type = ACTIVITY_MAP.get(activity)
    if activity_type is None:
        print(f"Unknown activity type '{activity}', skipping entry.")
        return

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Insert data into 'main' table, allowing NULL values for finish_time and note
        cursor.execute(
            """
            INSERT INTO main (activity_type, input_type, date, time, finish_time, note)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (activity_type, input_type, date, start_time, finish_time if finish_time else None, note if note else None)
        )

        # Commit and close connection
        conn.commit()
        print("Data inserted successfully!")

    except Exception as e:
        print("Error inserting data:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

    activity_logs = fetch_activity_data()
   
