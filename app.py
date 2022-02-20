""""Main functionality file, powering the backend of our site."""


from flask import Flask, render_template, request
from helpers import user, covid_result, find_sleep, find_water_intake
import http.client
import json

app: Flask = Flask(__name__)

users: list[user] = []
user_number: int = 0


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
        payload = json.dumps({
        "to": [
            f"+1{phone}"
        ],
        "from": "+19193913463",
        "text": "As of 12:05pm of February 18th, 2020:\nNewly Reported Cases: 4,871\nCurrently Hospitalized: 2,634\nDeaths: 22,148 deaths\nDaily Percent Positive: 10.3%\n75% of the adult population is vaccinated with at least one dose\nReminder to wear a mask, wash your hands, get vaccinated, and take other necessary health precautions<3",
        "applicationId": "1955b5c0-a0c0-498e-955a-719093718d6c",
        "media": "https://www1.pictures.livingly.com/mp/81ln60YcYdil.jpg?crop=1xw:1xh;center,top&resize=768:*",
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

    return render_template('resources.html')


@app.route('/survey', methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        global users
        global user_number

        fname: str = request.form['fname']
        lname: str = request.form['lname']
        phone: str = ""
        for character in request.form['number']:
            try: 
                phone_number: int = int(character)
                phone += str(phone_number)
            except:
                pass
        height: str = request.form['height']
        age: str = request.form['age']
        hours_sleep: str = request.form['sleep']
        mood: str = request.form['mood']
        energy_level: str = request.form['energy']

        # using helper functions to calculate recommendations
        recommended_water: str = find_water_intake(int(age))
        recommended_sleep: str = find_sleep(int(age))

        # TODO: put these variable just calculated into summary

        if fname == '' or lname == '':
            return render_template("survey.html")


        
        intro: str = f"Thanks for filling out the CommuniCares survey, {fname}. Based on your responses, here are some recommendations for your day. "
        water_message: str = f"It is recommended that you consume {recommended_water} ounces of water per day. Better get to hydrating! "
        sleep_message: str = f"Sleep is one of the most important forms of self care. Last night you slept for {hours_sleep} hours, and you are recommended to get {recommended_sleep} hours. Sweet dreams! "
        doctor_message: str = f"Based on your symptoms, it is recommended you seek guidance from a trusted medical professional. "
        summary: str = intro
        if request.form["important"] == 'water':
            summary = summary + water_message + sleep_message
        if request.form["important"] == 'sleep':
            summary = summary + sleep_message + water_message
        if request.form['important'] == 'physical':
            if request.form['symptoms'] != 'none':
                summary = summary + doctor_message + water_message + sleep_message
        elif request.form['important'] != 'physical':
            if request.form['symptoms'] != 'none':
                summary = summary + doctor_message
        
        new_user: user = user(user_number, fname, lname, summary)
        users.append(new_user)

        user_number += 1

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