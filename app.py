from flask import Flask
from flask import redirect, url_for, request, render_template, jsonify
from datetime import datetime




app = Flask(__name__)


@app.route('/')
def index():
    check = "testing please show!"
    return render_template('index.html', check = check)


@app.route('/submit', methods=['POST'])
def collect_form_data():
    """
    Collect form data sent via POST request.
    """
    # Get form data
    form_data = request.form.to_dict()
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
    print("Received form data:", form_data)

    return render_template('index.html', check = "will do later")



if __name__ == "__main__":
    app.run(debug=True)