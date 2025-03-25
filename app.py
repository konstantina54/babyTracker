from flask import Flask
from flask import redirect, render_template
import os
import pandas as pd
from functions import display_data, clean_manual_data, table_view, reorganise_data, nap_length, calculate_time_difference, collect_form_data


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    """ load main page """
    display_data()
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def form_submit():
    """ any activity submit """
    collect_form_data()
    return render_template('index.html')


@app.route('/second')
def index2():
    """ activity table """
    df = table_view()
    table_html = df.to_html(classes='table table-striped', index=False)
    return render_template('main.html',table=table_html)



if __name__ == "__main__":
    app.run(debug=True)