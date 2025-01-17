from flask import Flask
from flask import redirect, url_for, request, render_template, jsonify
from datetime import datetime
import json


app = Flask(__name__)


def display_data():
   with open('test.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # manual_data = line.find("ManualInput")
        # if manual_data > 1:
        data = clean_manual_data(line)
        # elif (line.find("AutoInput") > 1):
        #     # 2024-12-09 16:06:06 food AutoInput
        #     auto_data = line.replace(" AutoInput", "")           
            # data = auto_data.split(" ")
            # clean_automated_data(auto_data)
            # cleaned_data = [[row[0], row[1], row[2].strip()] for row in data]
            # print(auto_data)
           
            

def clean_manual_data(data):
    print(data + "this")
    # start_json = data.find("{")
    # if data.find(" M") >0:
    #     manual_inputs = data[start_json:last_json]
    # else data.find(" A") >0
    #    manual_inputs = data[start_json:last_json]

    # last_json = data.find(" M")
    # last_json = data.find(" A")
    manual_inputs = dict_str
    manual_inputs = manual_inputs.replace("'", "\"")
    # manual_inputs = manual_inputs.replace(" AutoInput", "")
    # manual_inputs = manual_inputs.replace(" ManualInput", "")
    print(manual_inputs)
    # res = json.loads(manual_inputs)
    # print(str(res))
    # print(type(res))
    # print(f"Date: {res['manualCalendar']}")
    # if 'sTime' in res:
    #     time_difference = calculate_time_difference(res['sTime'], res['fTime'])
    #     # print(f"Date: {res['manualCalendar']}")
    #     print(f"Time: {time_difference}")
    #     print(f"Activity: Nap Time")
    # elif 'foodTime' in res:
    #     # print(f"Date: {res['manualCalendar']}")
    #     print(f"Time: {res['foodTime']}")
    #     print(f"Activity: Food Time")
    # else:
    #     # print(f"Date: {res['manualCalendar']}")
    #     print(f"Time: {res['pottyTime']}")
    #     if 'no1' in res  and 'no2' in res:
    #         print(f"Activity: Potty Activity no1 and no2")
    #     elif 'no1' in res:
    #         print(f"Activity: Potty Activity no1")
    #     else: 
    #         print(f"Activity: Potty Activity no2")


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
    check = "Results"
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
# Need to change the transformed dict to include the potty activity and also to be able to do the sleeping activity
    if 'AutoCalendar' in form_data:
        if 'foodTime' in key:
            activity = 'foodTime'
        elif 'no1' in key or 'no2' in key:
            activity = 'pottyTime'

        else: 
            activity = 'sleepTime'

        transformed = f"{date} {{'manualCalendar': '{date}', '{activity}': '{current_time}'}}"
        with open('test.txt', 'a') as fd:
            fd.write(f'\n{transformed} AutoInput') 
    else:
        with open('test.txt', 'a') as fd:
            fd.write(f'\n{date} {form_data} ManualInput')
    return render_template('index.html', check = "results to displa maybe button?")


@app.route('/second')
def index2():
    check = "Results"
    # display_data()
    return render_template('main.html', check = check)    


if __name__ == "__main__":
    app.run(debug=True)