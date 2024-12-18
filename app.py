from flask import Flask
from flask import redirect, url_for, request, render_template, jsonify
from datetime import datetime
import json


app = Flask(__name__)


def display_data():
   with open('test.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        manual_data = line.find("ManualInput")
        if manual_data > 1:
            # print(line.strip())
            start_json = line.find("{")
            last_json = line.find(" M")
            manual_inputs = line[start_json:last_json]
            x = manual_inputs.replace("'", "\"")
            res = json.loads(x)
            print(str(res))
            print(type(res))
            clean_manual_data(res)
            date = res['manualCalendar']
        elif (line.find("AutoInput") > 1):
            # 2024-12-09 16:06:06 food AutoInput
            auto_data = line.replace(" AutoInput", "")           
            # data = auto_data.split(" ")
            clean_automated_data(auto_data)
            # cleaned_data = [[row[0], row[1], row[2].strip()] for row in data]
            # print(auto_data)
           
            

def clean_manual_data(data):
    date = data['manualCalendar']

    # Define rules for grouping
    rules = {
        "number_related": ["number"],
        "nap_related": ["nap"],
    }

    # Standardize groups
    groups = standardize_groups(data, rules)

    # Print results
    for group_name, group_data in groups.items():
        print(f"{group_name}: {group_data}")

            

def standardize_groups(data, rules):
    groups = {key: [] for key in rules.keys()}
    groups["others"] = []  # Default group for unmatched entries

    for entry in data:
        matched = False
        for group, keywords in rules.items():
            if any(keyword in entry['activity'].lower() for keyword in keywords):
                groups[group].append(entry)
                matched = True
                break
        if not matched:
            groups["others"].append(entry)

    return groups            



def clean_automated_data(data):
    parts = data.split(" ", 2)  # Split into up to 3 parts: date, time, and activity
    date, time, activity = parts  # Unpack into variables

    # Print the variables
    print(f"Date: {date}")
    print(f"Time: {time}")
    print(f"Activity: {activity}")
    return date, time, activity




@app.route('/')
def index():
    check = "Results"
    display_data()
    return render_template('index.html', check = check)


@app.route('/submit', methods=['POST'])
def collect_form_data():
    """
    Collect form data sent via POST request.
    """
    # Get form data
    form_data = request.form.to_dict()
    print("Received form data:", form_data)
    # on any submit get the current time?

    # Get current datetime
    current_datetime = datetime.now()

    # Convert to string
    datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    manual_date = current_datetime.strftime('%Y-%m-%d')
    for key in form_data:
        id_ = key.partition('.')[-1]
        value = request.form[key]
        if key.startswith('auto.'):
            with open('test.txt', 'a') as fd:
                fd.write(f'\n{datetime_string} {id_} AutoInput')
        else:
            with open('test.txt', 'a') as fd:
                fd.write(f'\n {manual_date} {form_data} ManualInput')
    # Print form data to the console (for debugging)
    return render_template('index.html', check = "results to displa maybe button?")


if __name__ == "__main__":
    app.run(debug=True)