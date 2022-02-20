from flask import Flask, render_template, request
from helpers import user, find_house, covid_result, find_sleep, find_water_intake
import http.client
import json

app: Flask = Flask(__name__)

users: list[user] = []
user_number: int = 0

# summary to be texted/result: 
recommended_sleep: int = 0
recommended_water: int = 0
water_message: str = f"Recommended Water Intake: {recommended_water} cups"
sleep_message: str = f"Recommended Sleep: {recommended_sleep} hours"
doctor_message: str = "It is recommended you go see a doctor." 

summary: str = (f"Summary report: ")

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/all-results')
def all_results():
    return render_template('all-results.html', users=users)


@app.route('/user<usernumber>')
def display_user(usernumber: str):
    return render_template('user.html', user=users[int(usernumber)])


@app.route('/resources')
def resources():
    if request.method == "post":
        global users 
        global user_number
        phone: str = ""
        covid: str = request.form['COVID']
        # message: str = ""

        covid_message: str = covid_result(covid)

        # here is the bandwidth API 
        conn = http.client.HTTPSConnection("messaging.bandwidth.com")
        if covid_message == "no":
            payload = json.dumps({
            "to": [
                f"+1{phone}"
            ],
            "from": "+19193913463",
            "text": "You have opted not to receive COVID updates. Have a good day :)",
            "media": "https://www1.pictures.livingly.com/mp/81ln60YcYdil.jpg",
            "tag": "covid message"
            })
        else:        
            payload = json.dumps({
            "to": [
                f"+1{phone}"
            ],
            "from": "+19193913463",
            "text": "As of 12:05pm of February 18th, 2020:\nNewly Reported Cases: 4,871\nCurrently Hospitalized: 2,634\nDeaths: 22,148 deaths\nDaily Percent Positive: 10.3%\n75% of the adult population is vaccinated with at least one dose\nReminder to wear a mask, wash your hands, get vaccinated, and take other necessary health precautions<3",
            "applicationId": "1955b5c0-a0c0-498e-955a-719093718d6c",
            "media": "https://www1.pictures.livingly.com/mp/81ln60YcYdil.jpg",
            "tag": "covid message"
            })
        headers = {
        'Authorization': 'Basic aGFja2F0aG9uXzAxOmYqdGdlcEd4QnlHVnRFQ1cmVzdXR2YzJFJ3Z1BNSA==',
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/api/v2/users/5008573/messages", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        # end Bandwidth API
    return render_template('resources.html')


@app.route('/survey', methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        global users
        global user_number

        fname: str = request.form['fname']
        lname: str = request.form['lname']
        # animal: str = request.form['animal']
        phone: str = ""
        for character in request.form['number']:
            try: 
                phone_number: int = int(character)
                phone += str(phone_number)
            except:
                pass
        height: str = request.form['height']
        age: str = request.form['age']
        # TODO: store other inputs as variables

        if fname == '' or lname == '':
            return render_template("survey.html")

        # house: str = find_house(animal)
        new_user: user = user(user_number, fname, lname, summary)
        users.append(new_user)

        user_number += 1

        # summary formatting
        # if "most important info" == "water":
            # summary = ""
        # if doctor
        if request.form['symptoms'] != 'none': 
            summary = summary + doctor_message 

        # here is the bandwidth API 
        conn = http.client.HTTPSConnection("messaging.bandwidth.com")
        payload = json.dumps({
        "to": [
            f"+1{phone}"
        ],
        "from": "+19193913463",
        "text": summary,
        "applicationId": "1955b5c0-a0c0-498e-955a-719093718d6c",
        "media": "https://i.imgur.com/pV8dKER.png",
        "tag": "test message"
        })
        headers = {
        'Authorization': 'Basic aGFja2F0aG9uXzAxOmYqdGdlcEd4QnlHVnRFQ1cmVzdXR2YzJFJ3Z1BNSA==',
        'Content-Type': 'application/json'
        }
        conn.request("POST", "/api/v2/users/5008573/messages", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        # end Bandwidth API
        return render_template("result.html", summary=summary)
    return render_template("survey.html")


if __name__ == '__main__':
    app.run(debug=True)