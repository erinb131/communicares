from flask import Flask, render_template, request
from helpers import user, find_house
import http.client
import json

app: Flask = Flask(__name__)


users: list[user] = []
user_number: int = 0

# summary to be texted/result: 
summary: str = ("Summary report: \n Idk \n 1234")

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
    return render_template('resources.html')


@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        global users
        global user_number

        fname: str = request.form['fname']
        lname: str = request.form['lname']
        animal: str = request.form['animal']
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
            return render_template("quiz.html")

        house: str = find_house(animal)
        new_user: user = user(user_number, fname, lname, house)
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
        "media": "https://static.wikia.nocookie.net/club-penguin-rewritten/images/9/95/Water_Droplet_Pin.png/revision/latest/top-crop/width/360/height/450?cb=20170720010752?crop=1xw:1xh;center,top&resize=768:*",
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
        return render_template("result.html", house=house)
    return render_template("quiz.html")


if __name__ == '__main__':
    app.run(debug=True)