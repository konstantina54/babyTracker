from flask import Flask
from flask import redirect, url_for, request, jsonify, flash
from datetime import datetime
import time, os
from dotenv import load_dotenv
import json, csv
import pandas as pd
from postgres_commands import sql_new_entry, sql_activity_list, calculate_duration

# should I add ioption to update notes with random input?2. Fetching Logs for the Dashboard View
# need to make sure the manual input is not date in the future. Block if the date is ahead


# def display_data():
#     """Open file with collected activities"""
#     with open('test.txt', 'r') as file:
#         for line in file:
#             data = clean_manual_data(line)
#             # display_formating(data)


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



# def clean_manual_data(data):
#     """ Transform data for display"""
#     # used by the txt file. Is it really needed?
#     data = data.replace("'", '"')
#     if not data.strip():
#         print("error")
#     else:
#         activity_data = json.loads(data)
#         return activity_data



def table_view():
    """ Transform data for table view loading in df ignoring any empty rows"""
    with open('test.txt', 'r') as file:
        # read lines from the file
        lines = file.readlines()
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
    if 'customer_note' in form_data:
        print(form_data['customer_note'])
        # update db
        
    elif 'AutoCalendar' in form_data:
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
                    activity_type = "sleep"
                    input_type = 'auto'
                    date = x['manualCalendar']
                    start_time = x['sTime']
                    finish_time = x['fTime']
                    note = calculate_duration(start_time, finish_time)
                    sql_new_entry(activity_type,input_type, date, start_time, finish_time, note)
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
            activity_type = 'sleep'
            start_time = form_data['sTime']
            finish_time = form_data['fTime']
            # check if it calculates correctly the nap length
            note = calculate_duration(start_time, finish_time)        
        sql_new_entry(activity_type,input_type, date, start_time, finish_time, note)


def download_activity():
    selected_activity = request.form.get("activityFilter")
    activity_results = sql_activity_list(selected_activity)
    file_path = "activity_export.csv"
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Start Time', 'Activity Type', 'Finish Time', 'Note'])  # Header
            writer.writerows(activity_results)