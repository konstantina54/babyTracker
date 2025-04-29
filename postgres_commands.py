import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv(override=True)

# PostgreSQL connection details
DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
    }


def fetch_activity_data():
    """Fetches activity records from the PostgreSQL database."""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # SQL query to retrieve relevant data
        cursor.execute("""
            SELECT date, time, activity_type, finish_time, note FROM main WHERE activity_type != '' ORDER BY date DESC;
        """)

        # Fetch all records from the query
        records = cursor.fetchall()

        # Convert list of tuples into Pandas DataFrame
        df = pd.DataFrame(records, columns=['Date', 'Start Time', 'Activity Type','Finish Time', 'Note'])

        # Only update notes for Sleep activities
        sleep_mask = (df['Activity Type'] == "Sleep") & (df['Finish Time'].notna()) & (df['Start Time'].notna())

        df.loc[sleep_mask, 'Note'] = df[sleep_mask].apply(
            lambda row: calculate_duration(row['Start Time'], row['Finish Time']),
            axis=1
        )

        # Drop Finish Time column
        df.drop(columns=['Finish Time'], inplace=True)
        # Remove none values
        df["Note"].fillna("", inplace = True)
        # Capitalize activity types
        df['Activity Type'] = df['Activity Type'].str.capitalize()
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
        start_time = datetime.strptime(start_time_obj, "%H:%M").time()
        finish_time = datetime.strptime(finish_time_obj, "%H:%M").time()
        today = datetime.today().date()
        start_dt = datetime.combine(today, start_time)
        finish_dt = datetime.combine(today, finish_time)

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
    if activity is None:
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
            (activity, input_type, date, start_time, finish_time if finish_time else None, note if note else None)
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
   

def sql_activity_list(activity):
    """Fetches activity records from the PostgreSQL database filtered for download."""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        if activity is not None:
            cursor.execute("""
                SELECT date, time, activity_type, finish_time, note
                FROM main
                WHERE activity_type = %s
                ORDER BY date DESC;
            """, (activity,))
            rows = cursor.fetchall()
        else:
            print("Invalid activity name:", activity)
        return rows
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def sql_update(update_data):
    """Update activity in postgres"""
    # need to find a way to identify which record I am updating????
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        if activity is not None:
            cursor.execute("""
                UPDATE main
                SET color = 'red'
                WHERE brand = 'Volvo'; 
            """, (activity,))
            rows = cursor.fetchall()
        else:
            print("Invalid activity name:", activity)
        return rows
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()   
