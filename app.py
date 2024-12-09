from flask import Flask
from flask import redirect, url_for, request, render_template, jsonify
from datetime import datetime
import json




app = Flask(__name__)


def display_data():
   with open('test.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        date = ""
        time = ""
        activity = ""

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
        elif (line.find("AutoInput") > 1):
            # 2024-12-09 16:06:06 food AutoInput
            auto_data = line.replace(" AutoInput", "")           
            y = auto_data.split(" ")
            print(y)
            # res1 = json.loads(y)
            # print(str(res1))
            # print(type(res1))






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