from flask import Flask
from flask import redirect, render_template, request, url_for
import os
import pandas as pd
from functions import table_view, data_to_sql, download_activity
from postgres_commands import fetch_activity_data


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    """ load main page """
    # display_data() 
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def form_submit():
    """ any activity submit """
    # collect_form_data()
    if request.form.get("results") == 'Download Results':
        download_activity()
        return ('', 204)
    else:
        data_to_sql()
        # add message showing that activity is added
        return ('', 204)


@app.route('/second')
def index2():
    """ Renders activity table from PostgreSQL """
    df = fetch_activity_data()  # Fetch data from the database
    table_html = df.to_html(classes='table table-striped', index=False, table_id= "activityTable")  # Convert to HTML table
    return render_template('main.html', table=table_html)  # Pass table to template




if __name__ == "__main__":
    app.run(debug=True)