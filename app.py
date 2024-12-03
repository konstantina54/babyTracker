from flask import Flask
from flask import redirect, url_for, request, render_template




app = Flask(__name__)


@app.route('/', methods =["GET", "POST"])
def gfg():
    check = "testing please show!"
    # if request.method == "POST":
    #    # getting input with name = fname in HTML form
    #    first_name = request.form.get("sleepTime")
    #    # getting input with name = lname in HTML form 
    #    last_name = request.form.get("food") 
    #    return "Your name is "+first_name + last_name
    # elif request.method == "GET":
    #     print(request.form.get("napStart"))
    # else:
    #     print("somethings wrong")
    return render_template('index.html', check = check)




if __name__ == "__main__":
    app.run()