from flask import Flask
from flask import redirect, url_for, request, render_template




app = Flask(__name__)

@app.route('/')
def collectData():
    # button_id = request.form['id']
    # print(button_id)
    check = "testing please show!"
    # print(request.form.get("search"))
    return render_template('index.html', check = check)











if __name__ == "__main__":
    app.run()