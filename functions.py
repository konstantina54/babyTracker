from flask import Flask
from flask import redirect, url_for, request, jsonify, flash
from datetime import datetime
import time
import json
import psycopg2
import pandas as pd


DB_CONFIG = {
    "dbname": "baby_tracker",  # Replace with your database name
    "user": "postgres",         # Replace with your username
    "password": "Learner1",     # Replace with your password
    "host": "localhost",             # Host, default is localhost
    "port": "5432",                  # Default port for PostgreSQL
}


def display_data():
    """Open file with collected activities"""
    with open('test.txt', 'r') as file:
        for line in file:
            # print(line)
            data = clean_manual_data(line)
            # display_formating(data)


def calculate_time_difference(start_time, end_time):
    # Calculating time between naps
    def time_to_minutes(time_str):
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    def minutes_to_time(total_minutes):
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02}:{minutes:02}"
    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)

    time_diff_minutes = end_minutes - start_minutes

    if time_diff_minutes < 0:
        time_diff_minutes += 24 * 60
    return minutes_to_time(time_diff_minutes)



def clean_manual_data(data):
    """ Transform data for display"""
    data = data.replace("'", '"')
    # manual_inputs = manual_inputs.replace("'", '"')
    if not data.strip():
        print("error")
    else:
        activity_data = json.loads(data)
        return activity_data



def table_view():
    """ Transform data for table view loading in df ignoring any empty rows"""
    with open('test.txt', 'r') as file:
        # read lines from the file
        lines = file.readlines()
        # reorg = reorganise_data(lines)
        res = []
        # date time activity note
        for line in lines:
            line = line.replace("'", '"')
            if line.strip():
                activity_data = json.loads(line)
                res.append(activity_data)
        new_format = reorganise_data(res)    
        df = pd.json_normalize(res)
        df2 = pd.json_normalize(new_format)
        df.fillna('', inplace=True)
        return df2        


def reorganise_data(data):
    """ Transform data if unified form for collection in file"""
    organised_data = []
    for row in data:
        date = row.get('manualCalendar', '')
        other = ''

        if 'foodTime' in row:
            time = row['foodTime']
            activity = 'Food'
        elif 'pottyTime' in row:
            time = row['pottyTime']
            activity = 'Potty'
            if 'no1' in row or 'no2' in row:
                if 'no1' in row and 'no2' in row:
                    other = 'No1 and No2'
                elif 'no1' in row:
                    other = 'No1'
                elif 'no2' in row:
                    other = 'No2'
        elif 'sTime' in row and row['sTime'] and row['fTime']:
            time = row['sTime']
            activity = 'Nap'
            start_time = datetime.strptime(row['sTime'], "%H:%M")
            finish_time = datetime.strptime(row['fTime'], "%H:%M")
            total_minutes = (finish_time - start_time).total_seconds() / 60
            hours = int(total_minutes // 60)
            minutes = int(total_minutes % 60)
            other = f"{hours}.{minutes:02d} h"
        else:
            time = ''
            activity = 'Unknown'

        organised_data.append({'Date': date, 'Time': time, 'Activity': activity, 'Note': other})
    return organised_data



def nap_length(activity):
    """ Making sure start nap button is pressed before finish and calculating time"""
    if not hasattr(nap_length, "datetime_start"):
        nap_length.datetime_start = None
        nap_length.start_time = None

    if 'sTime' in activity: 
        nap_length.datetime_start = datetime.now()
        nap_length.start_time = f"{nap_length.datetime_start.hour}:{nap_length.datetime_start.minute:02d}"
        print(f"Start time recorded: {nap_length.start_time}")


    elif 'fTime' in activity:
        if nap_length.datetime_start is None: 
            flash("Error: Start time not set.")
        

        datetime_finish = datetime.now()
        finish_time = f"{datetime_finish.hour}:{datetime_finish.minute:02d}"

        if nap_length.datetime_start is not None and datetime_finish > nap_length.datetime_start:  # Validate time order
            date = datetime_finish.date()
            transformed = {
                "manualCalendar": str(date),
                "sTime": nap_length.start_time,
                "fTime": finish_time,
                "InputType": "Auto"
            }
            print(f"Nap data recorded: {transformed}")
            # Reset start time for the next activity
            nap_length.datetime_start = None
            nap_length.start_time = None
            return transformed
        else:
            flash("Error: Finish time must be after start time.", 'danger')
            pass


def collect_form_data():
    # Get form data
    form_data = request.form.to_dict()
    print("Received form data:", form_data)
    # on any submit get the current time?
    data_to_sql(form_data)
    # Get current datetime
    current_datetime = datetime.now()
    current_time = f"{current_datetime.hour}:{current_datetime.minute}"

    # Convert to string and add to file
    datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    date = current_datetime.strftime('%Y-%m-%d')
    activity = ''
    transformed = ''
    if 'AutoCalendar' in form_data:
        if 'foodTime' in form_data:
            activity = 'foodTime'
            transformed = f"{{'manualCalendar': '{date}', '{activity}': '{current_time}', 'InputType' : 'Auto'}}"
        elif 'no1' in form_data or 'no2' in form_data or 'both' in form_data:
            activity = 'pottyTime'
            if 'both' in form_data:
                transformed = f"{{'manualCalendar': '{date}', '{activity}': '{current_time}', 'no1': 'on', 'no2': 'on', 'InputType' : 'Auto'}}"
            elif 'no1' in form_data:
                transformed = f"{{'manualCalendar': '{date}', '{activity}': '{current_time}', 'no1': '{form_data['no1']}', 'InputType' : 'Auto'}}"
            elif 'no2' in form_data:
                transformed = f"{{'manualCalendar': '{date}', '{activity}': '{current_time}', 'no2': '{form_data['no2']}', 'InputType' : 'Auto'}}"
        else:
            if 'sTime' in form_data or 'fTime' in form_data:
                x = nap_length(form_data)
                if x is not None:
                    transformed = x

        with open('test.txt', 'a') as fd:
                fd.write(f'\n{transformed}') 
    else:
        form_data['InputType'] = 'Manual'
        with open('test.txt', 'a') as fd:
            fd.write(f'\n{form_data}')



def data_to_sql(form_data):
    # form_data = request.form.to_dict()
    # Get current datetime
    # needed for sql function activity_type, input_type, date, start_time, finish_time, note
    current_datetime = datetime.now()
    # current_time = f"{current_datetime.hour}:{current_datetime.minute}"
    current_time = time.strftime("%H:%M:%S", time.localtime())
    # Convert to string and add to file
    datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    date = current_datetime.strftime('%Y-%m-%d')

    activity_type = ''
    input_type = ''
    finish_time = ''
    note = ''
    if 'AutoCalendar' in form_data:
        input_type = 'auto'
        if 'foodTime' in form_data:
            activity_type = 'food'
        elif any(key in form_data for key in ['no1', 'no2', 'both']):  
            activity_type = 'potty' 
            note = ' and '.join([key.capitalize() for key in ['no1', 'no2', 'both'] if key in form_data])
        else:
            if 'sTime' in form_data or 'fTime' in form_data:
                x = nap_length(form_data)
                if x is not None:
                    transformed = x
        sql_new_entry(activity_type,input_type, date, current_time, finish_time, note)           
    else:
        input_type = 'manual'




def sql_new_entry(activity, input_type, date, start_time, finish_time, note):
    # establishing the connection
    print(activity, input_type, date, start_time, finish_time, note)
    DB_CONFIG = {
    
    }

    ACTIVITY_MAP = {
    "foodTime": 1,   # food
    "sTime": 2,      # sleep
    "pottyTime": 3   # potty
    }

    activity_type = None
    for key, act_id in ACTIVITY_MAP.items():
        if key == activity:
            activity_type = act_id
            print(activity_type)
            break

    if not activity_type:
        print("Unknown activity type, skipping entry:", activity)
        return

    try:
    # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
            # Insert data into 'main' table
        cursor.execute(
            """
            INSERT INTO main (activity_type, input_type, date, time, finish_time, note)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (activity_type, input_type, date, start_time, finish_time, note)
        )

        # Commit and close connection
        conn.commit()
        print("Data inserted successfully:", form_data)

    except Exception as e:
        print("Error inserting data:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()








# # Database connection details
# DB_CONFIG = {
#     "dbname": "your_database",
#     "user": "your_user",
#     "password": "your_password",
#     "host": "localhost",
#     "port": "5432",
# }

# # Mapping input keys to activity IDs (as per predefined entries in 'activity' table)
# ACTIVITY_MAP = {
#     "foodTime": 1,   # food
#     "sTime": 2,      # sleep
#     "pottyTime": 3   # potty
# }

# def insert_activity_record(form_data):
#     """Processes form data and inserts it into the 'main' table."""
#     try:
#         # Connect to PostgreSQL
#         conn = psycopg2.connect(**DB_CONFIG)
#         cursor = conn.cursor()




