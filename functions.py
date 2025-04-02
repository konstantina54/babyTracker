from flask import Flask
from flask import redirect, url_for, request, jsonify, flash
from datetime import datetime
import time, os
from dotenv import load_dotenv
import json
import psycopg2
import pandas as pd



DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

load_dotenv(override=True)

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


# def reorganise_data(data):
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



def nap_data_collected(activity):
    """ Making sure start nap button is pressed before finish and calculating time"""
    if not hasattr(nap_data_collected, "datetime_start"):
        nap_data_collected.datetime_start = None
        nap_data_collected.start_time = None

    if 'sTime' in activity: 
        nap_data_collected.datetime_start = datetime.now()
        nap_data_collected.start_time = f"{nap_data_collected.datetime_start.hour}:{nap_data_collected.datetime_start.minute:02d}"
        print(f"Start time recorded: {nap_data_collected.start_time}")


    elif 'fTime' in activity:
        if nap_data_collected.datetime_start is None: 
            flash("Error: Start time not set.")
        

        datetime_finish = datetime.now()
        finish_time = f"{datetime_finish.hour}:{datetime_finish.minute:02d}"

        if nap_data_collected.datetime_start is not None and datetime_finish > nap_data_collected.datetime_start:  # Validate time order
            date = datetime_finish.date()
            transformed = {
                "manualCalendar": str(date),
                "sTime": nap_data_collected.start_time,
                "fTime": finish_time,
                "InputType": "Auto"
            }
            print(f"Nap data recorded: {transformed}")
            # Reset start time for the next activity
            nap_data_collected.datetime_start = None
            nap_data_collected.start_time = None
            return transformed
        else:
            flash("Error: Finish time must be after start time.", 'danger')
            pass


# def collect_form_data():
#     # Get form data
#     form_data = request.form.to_dict()
#     print("Received form data:", form_data)
#     # on any submit get the current time?
#     data_to_sql(form_data)
#     # Get current datetime
#     current_datetime = datetime.now()
#     current_time = f"{current_datetime.hour}:{current_datetime.minute}"

#     # Convert to string and add to file
#     datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
#     date = current_datetime.strftime('%Y-%m-%d')
#     activity = ''
#     transformed = ''
#     if 'AutoCalendar' in form_data:
#         if 'foodTime' in form_data:
#             activity = 'foodTime'
#             transformed = f"{{'manualCalendar': '{date}', '{activity}': '{current_time}', 'InputType' : 'Auto'}}"
#         elif 'no1' in form_data or 'no2' in form_data or 'both' in form_data:
#             activity = 'pottyTime'
#             if 'both' in form_data:
#                 transformed = f"{{'manualCalendar': '{date}', '{activity}': '{current_time}', 'no1': 'on', 'no2': 'on', 'InputType' : 'Auto'}}"
#             elif 'no1' in form_data:
#                 transformed = f"{{'manualCalendar': '{date}', '{activity}': '{current_time}', 'no1': '{form_data['no1']}', 'InputType' : 'Auto'}}"
#             elif 'no2' in form_data:
#                 transformed = f"{{'manualCalendar': '{date}', '{activity}': '{current_time}', 'no2': '{form_data['no2']}', 'InputType' : 'Auto'}}"
#         else:
#             if 'sTime' in form_data or 'fTime' in form_data:
#                 x = nap_data_collected(form_data)
#                 if x is not None:
#                     transformed = x

#         with open('test.txt', 'a') as fd:
#                 fd.write(f'\n{transformed}') 
#     else:
#         form_data['InputType'] = 'Manual'
#         with open('test.txt', 'a') as fd:
#             fd.write(f'\n{form_data}')



def data_to_sql():
    form_data = request.form.to_dict()
    print("Received form data:", form_data)
    # needed for sql function activity_type, input_type, date, start_time, finish_time, note
    current_datetime = datetime.now()
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
                # calculating nap start time and end time reformating for postgres
                x = nap_data_collected(form_data)
                if x is not None:
                    activity_type = "sTime"
                    input_type = 'auto'
                    date = x['manualCalendar']
                    current_time = x['sTime']
                    finish_time = x['fTime']
    else:
        input_type = 'manual'
        date = form_data['manualCalendar']
        if 'foodTime' in form_data:
            activity_type = 'food'
            start_time = form_data['foodTime']
        elif any(key in form_data for key in ['no1', 'no2', 'both']):  
            activity_type = 'potty'
            start_time = form_data['pottyTime']
            note = ' and '.join([key.capitalize() for key in ['no1', 'no2', 'both'] if key in form_data])
        elif 'sTime' in form_data or 'fTime' in form_data:
            activity_type = 'sTime'
            start_time = form_data['sTime']
            finish_time = form_data['fTime']
            
    sql_new_entry(activity_type,input_type, date, current_time, finish_time, note)





def sql_new_entry(activity, input_type, date, start_time, finish_time = None, note = None):
    # establishing the connection
    print(activity, input_type, date, start_time, finish_time, note)
    # DB_CONFIG = {
    #     "database":"baby_tracker",
    #     'user':'postgres',
    #     'password':'Learner1',
    #     'host':'localhost',
    #     'port':'5432'
    # }

    # ACTIVITY_MAP = {
    # "food": 1,   # food
    # "sTime": 2,  # sleep
    # "potty": 3   # potty
    # }

    # activity_type = ACTIVITY_MAP.get(activity)
    # if activity_type is None:
    #     print(f"Unknown activity type '{activity}', skipping entry.")
    #     return

    # try:
    #     # Connect to PostgreSQL
    #     conn = psycopg2.connect(**DB_CONFIG)
    #     cursor = conn.cursor()

    #     # Insert data into 'main' table, allowing NULL values for finish_time and note
    #     cursor.execute(
    #         """
    #         INSERT INTO main (activity_type, input_type, date, time, finish_time, note)
    #         VALUES (%s, %s, %s, %s, %s, %s)
    #         """,
    #         (activity_type, input_type, date, start_time, finish_time if finish_time else None, note if note else None)
    #     )

    #     # Commit and close connection
    #     conn.commit()
    #     print("Data inserted successfully!")

    # except Exception as e:
    #     print("Error inserting data:", e)

    # finally:
    #     if 'cursor' in locals():
    #         cursor.close()
    #     if 'conn' in locals():
    #         conn.close()

    # activity_logs = fetch_activity_data()
    # for entry in activity_logs:
    #     print(f"📅 {entry['date']} ⏰ {entry['start_time']} 🏷 {entry['activity']} 📝 {entry['note']}")








