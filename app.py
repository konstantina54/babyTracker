from flask import Flask
from flask import redirect, url_for, request, render_template, jsonify
from datetime import datetime
import json
import pandas as pd
# from functios import display_data, clean_manual_data


app = Flask(__name__)


def display_data():
   with open('test.txt', 'r') as file:
    # Read each line in the file
        # df = pd.DataFrame(file)
        # print(df)
    for line in file:
        # print(line)
        data = clean_manual_data(line)
        display_formating(data)

           
            

def clean_manual_data(data):
    print(data + "this")
    data = data.replace("'", '"')
    # manual_inputs = manual_inputs.replace("'", '"')
    activity_data = json.loads(data)
    return activity_data



def display_formating(activity_data):
    print(str(activity_data))        
    # print(type(activity_data))
    # date time activity
    date = activity_data['manualCalendar']
    if 'sTime' in activity_data:
        if len(activity_data["fTime"]) > 0 and len(activity_data["sTime"]) > 0:
            time_difference = calculate_time_difference(activity_data['sTime'], activity_data['fTime'])
            # print(f"Date: {activity_data['manualCalendar']}")
            print(f"Time: {time_difference}")
            print(f"Activity: Nap Time")


    elif 'foodTime' in activity_data:
        # print(f"Date: {activity_data['manualCalendar']}")
        print(f"Time: {activity_data['foodTime']}")
        print(f"Activity: Food Time")
    else:
        # print(f"Date: {activity_data['manualCalendar']}")
        print(f"Time: {activity_data['pottyTime']}")
        if 'no1' in activity_data  and 'no2' in activity_data:
            print(f"Activity: Potty Activity no1 and no2")
        elif 'no1' in activity_data:
            print(f"Activity: Potty Activity no1")
        else: 
            print(f"Activity: Potty Activity no2")


def calculate_time_difference(start_time, end_time):
    # Convert 'HH:MM' to total minutes since midnight
    def time_to_minutes(time_str):
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    # Convert total minutes back to 'HH:MM'
    def minutes_to_time(total_minutes):
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02}:{minutes:02}"

    # Calculate minutes for both times
    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)

    # Compute the difference
    time_diff_minutes = end_minutes - start_minutes

    # Handle cases where the end time is on the next day
    if time_diff_minutes < 0:
        time_diff_minutes += 24 * 60  # Add 24 hours in minutes

    # Return the difference in 'HH:MM' format
    return minutes_to_time(time_diff_minutes)      




@app.route('/')
def index():
    check = "activity_dataults"
    display_data()
    return render_template('index.html', check = check)


@app.route('/submit', methods=['POST'])
def collect_form_data():
    # Get form data
    form_data = request.form.to_dict()
    print("Received form data:", form_data)
    # on any submit get the current time?

    # Get current datetime
    current_datetime = datetime.now()
    current_time = f"{current_datetime.hour}:{current_datetime.minute}"

    # Convert to string
    datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    date = current_datetime.strftime('%Y-%m-%d')
    activity = ''
    transformed = ''
# Need to change the transformed dict to include the potty activity and also to be able to do the sleeping activity
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
            # if sTime create the line but wait until fTime is triggered and add to the line the time. Then add to file. Check if ftime is after stime 
            if 'sTime' in form_data or 'fTime' in form_data:
                transformed = nap_length(form_data)

        with open('test.txt', 'a') as fd:
            fd.write(f'\n{transformed}') 
    else:
        form_data['InputType'] = 'Manual'
        with open('test.txt', 'a') as fd:
            fd.write(f'\n{form_data}')
    return render_template('index.html', check = "activity_dataults to displa maybe button?")


@app.route('/second')
def index2():
    # display_data()
    df = table_view()
    table_html = df.to_html(classes='table table-striped', index=False)
    return render_template('main.html',table=table_html)





def table_view():
    with open('test.txt', 'r') as file:
        # read lines from the file
        lines = file.readlines()
        # reorg = reorganise_data(lines)
        res = []
        for line in lines:
            line = line.replace("'", '"')
            activity_data = json.loads(line)
            res.append(activity_data)
        new_format = reorganise_data(res)    
        df = pd.json_normalize(res)
        df2 = pd.json_normalize(new_format)
        df.fillna('', inplace=True)
        return df2




def reorganise_data(data):
    organised_data = []
    for row in data:
        date = row.get('manualCalendar', '')
        other = ''
        
        # Extract time and activity details
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
        elif 'sTime' in row and row['sTime']:
            time = row['sTime']
            activity = 'Start'
        elif 'fTime' in row and row['fTime']:
            time = row['fTime']
            activity = 'Finish'
        else:
            time = ''
            activity = 'Unknown'

        organised_data.append({'Date': date, 'Time': time, 'Activity': activity, 'Other': other})
    return organised_data
        

def nap_length(activity):
    if not hasattr(nap_length, "datetime_start"):
        nap_length.datetime_start = None
        nap_length.start_time = None

    # Button press logic
    if 'sTime' in activity:  # Start time button pressed
        nap_length.datetime_start = datetime.now()
        nap_length.start_time = f"{nap_length.datetime_start.hour}:{nap_length.datetime_start.minute:02d}"
        print(f"Start time recorded: {nap_length.start_time}")
         # Start time set, waiting for finish time

    elif 'fTime' in activity:  # Finish time button pressed
        if nap_length.datetime_start is None:  # Check if start time exists
            print("Error: Start time not set.")
        

        datetime_finish = datetime.now()
        finish_time = f"{datetime_finish.hour}:{datetime_finish.minute:02d}"

        if datetime_finish > nap_length.datetime_start:  # Validate time order
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
            print("Error: Finish time must be after start time.")
    else:
        print("Invalid button pressed. Use 'sTime' or 'fTime'.")



if __name__ == "__main__":
    app.run(debug=True)