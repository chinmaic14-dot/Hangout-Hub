import os
import io
import requests

from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, redirect, url_for, send_file

from flask_sqlalchemy import SQLAlchemy

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hangout.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)



# ---------------- DATABASE TABLES ----------------


class Event(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    location = db.Column(db.String(100))
    members = db.Column(db.Integer)



class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), default="Untitled Image")

class Poll(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    category = db.Column(db.String(100))

    option1 = db.Column(db.String(100))
    option2 = db.Column(db.String(100))
    option3 = db.Column(db.String(100))
    option4 = db.Column(db.String(100))

    votes1 = db.Column(db.Integer, default=0)
    votes2 = db.Column(db.Integer, default=0)
    votes3 = db.Column(db.Integer, default=0)
    votes4 = db.Column(db.Integer, default=0)



class SavedTrip(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    destination = db.Column(db.String(100))

    budget = db.Column(db.Integer)

    friends = db.Column(db.Integer)

    duration = db.Column(db.String(50))

    plan = db.Column(db.Text)



with app.app_context():

    db.create_all()



# ---------------- HOME ----------------


@app.route("/")
def home():

    return render_template("index.html")



# ---------------- CREATE EVENT ----------------


@app.route("/create", methods=["GET", "POST"])
def create():

    if request.method == "POST":

        event = Event(
            title=request.form["title"],
            category=request.form["category"],
            description=request.form["description"],
            date=request.form["date"],
            time=request.form["time"],
            location=request.form["location"],
            members=request.form["members"]
        )

        db.session.add(event)
        db.session.commit()

        return redirect(url_for("create"))

    events = Event.query.all()

    return render_template(
        "create_event.html",
        events=events
    )



@app.route("/my-events")
def my_events():

    events = Event.query.all()

    return render_template(
        "my_events.html",
        events=events
    )
@app.route("/delete-event/<int:event_id>")
def delete_event(event_id):

    event = Event.query.get_or_404(event_id)

    db.session.delete(event)

    db.session.commit()

    return redirect(url_for("my_events"))


@app.route("/edit-event/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):

    event = Event.query.get_or_404(event_id)

    if request.method == "POST":

        event.title = request.form["title"]
        event.category = request.form["category"]
        event.description = request.form["description"]
        event.date = request.form["date"]
        event.time = request.form["time"]
        event.location = request.form["location"]
        event.members = request.form["members"]

        db.session.commit()

        return redirect(url_for("my_events"))

    return render_template("edit_event.html", event=event)
# ---------------- GALLERY ----------------

@app.route("/gallery", methods=["GET","POST"])
def gallery():

    if request.method == "POST":

        image = request.files["image"]

        if image.filename != "":

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.static_folder,
                    "uploads",
                    filename
                )
            )

            new_image = Image(
                filename=filename,
                name=filename
            )

            db.session.add(new_image)
            db.session.commit()


    images = Image.query.all()

    return render_template(
        "gallery.html",
        images=images
    )


@app.route("/delete-image/<int:image_id>")
def delete_image(image_id):

    image = Image.query.get_or_404(image_id)

    file_path = os.path.join(
        app.static_folder,
        "uploads",
        image.filename
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(image)
    db.session.commit()

    return redirect(url_for("gallery"))


@app.route("/edit-image/<int:image_id>", methods=["GET", "POST"])
def edit_image(image_id):

    image = Image.query.get_or_404(image_id)

    if request.method == "POST":

        image.name = request.form["name"]

        db.session.commit()

        return redirect(url_for("gallery"))

    return render_template(
        "edit_image.html",
        image=image
    )



# ---------------- POLL ----------------


@app.route("/poll", methods=["GET","POST"])
def poll():

    if request.method == "POST":

        new_poll = Poll(

            category=request.form["category"],

            option1=request.form["option1"],

            option2=request.form["option2"],

            option3=request.form["option3"],

            option4=request.form["option4"]

        )


        db.session.add(new_poll)

        db.session.commit()


        return redirect(url_for("poll"))



    polls = Poll.query.all()


    return render_template(
        "poll.html",
        polls=polls
    )





@app.route("/vote/<int:poll_id>/<int:option>")
def vote(poll_id, option):

    poll = Poll.query.get_or_404(poll_id)



    if option == 1:

        poll.votes1 += 1

    elif option == 2:

        poll.votes2 += 1

    elif option == 3:

        poll.votes3 += 1

    elif option == 4:

        poll.votes4 += 1



    db.session.commit()


    return redirect(url_for("poll"))
@app.route("/delete-poll/<int:poll_id>")
def delete_poll(poll_id):

    poll = Poll.query.get_or_404(poll_id)

    db.session.delete(poll)
    db.session.commit()

    return redirect(url_for("poll"))



@app.route("/edit-poll/<int:poll_id>", methods=["GET","POST"])
def edit_poll(poll_id):

    poll = Poll.query.get_or_404(poll_id)

    if request.method == "POST":

        poll.category = request.form["category"]
        poll.option1 = request.form["option1"]
        poll.option2 = request.form["option2"]
        poll.option3 = request.form["option3"]
        poll.option4 = request.form["option4"]

        db.session.commit()

        return redirect(url_for("poll"))

    return render_template(
        "edit_poll.html",
        poll=poll
    )




# ---------------- AI PLANNER ----------------



def generate_plan(destination, budget, friends, duration, places, packing, cost_option, manual_cost):


    if places.strip():

        activities = places.split(",")

    else:

        activities = [
            "Explore nearby attractions",
            "Try local food",
            "Photography and fun activities"
        ]



    if packing.strip():

        packing_list = packing

    else:

        packing_list = "No packing items added"



    total = int(budget)

    people = int(friends)



    if cost_option == "manual" and manual_cost.strip():

        person_cost = int(manual_cost)

    else:

        person_cost = int(total / people)





    plan = f"""

🤖 AI Generated Trip Plan


📍 Destination: {destination}


👥 Number of Friends: {friends}


⏳ Duration: {duration}



📅 Suggested Schedule:

"""



    for i, activity in enumerate(activities):

        plan += f"""

Day {i+1}

• {activity.strip()}

• Enjoy sightseeing and create memories

"""



    plan += f"""



💰 Budget Estimation:


🚗 Travel : ₹{int(total*0.30)}


🍴 Food : ₹{int(total*0.30)}


🏨 Stay : ₹{int(total*0.20)}


🎡 Activities : ₹{int(total*0.15)}


⚠️ Emergency : ₹{int(total*0.05)}



👤 Cost Per Person:

₹{person_cost}



🎒 Packing Checklist:


{packing_list}



✨ Have a safe and enjoyable trip!

"""


    return plan

@app.route("/planner", methods=["GET", "POST"])
def planner():

    print("Planner route reached")

    result = None

    if request.method == "POST":

        print("POST received")

        destination = request.form["destination"]
        budget = request.form["budget"]

        friends = request.form["friends"]

        duration = request.form["duration"]

        places = request.form["places"]

        packing = request.form["packing"]

        cost_option = request.form["cost_option"]

        manual_cost = request.form["manual_cost"]



        result = generate_plan(
            destination,
            budget,
            friends,
            duration,
            places,
            packing,
            cost_option,
            manual_cost
        )
        print(result)



        new_trip = SavedTrip(

            destination=destination,

            budget=int(budget),

            friends=int(friends),

            duration=duration,

            plan=result

        )


        db.session.add(new_trip)

        db.session.commit()



    trips = SavedTrip.query.all()



    return render_template(
        "planner.html",
        result=result,
        trips=trips
    )

# ---------------- DELETE TRIP ----------------

@app.route("/delete-trip/<int:trip_id>")
def delete_trip(trip_id):

    trip = SavedTrip.query.get_or_404(trip_id)

    db.session.delete(trip)

    db.session.commit()

    return redirect(url_for("planner"))



# ---------------- EDIT TRIP ----------------

@app.route("/edit-trip/<int:trip_id>", methods=["GET", "POST"])
def edit_trip(trip_id):

    trip = SavedTrip.query.get_or_404(trip_id)


    if request.method == "POST":

        trip.destination = request.form["destination"]

        trip.budget = request.form["budget"]

        trip.friends = request.form["friends"]

        trip.duration = request.form["duration"]

        trip.plan = request.form["plan"]


        db.session.commit()


        return redirect(url_for("planner"))



    return render_template(
        "edit_trip.html",
        trip=trip
    )



# ---------------- DOWNLOAD SAVED TRIP PDF ----------------

@app.route("/download-trip/<int:trip_id>")
def download_trip(trip_id):

    trip = SavedTrip.query.get_or_404(trip_id)


    pdf = io.BytesIO()


    doc = SimpleDocTemplate(pdf)


    styles = getSampleStyleSheet()


    content = []


    content.append(

        Paragraph(
            "Hangout Hub Trip Plan",
            styles["Title"]
        )

    )


    content.append(Spacer(1,20))


    content.append(

        Paragraph(
            f"Destination: {trip.destination}",
            styles["Normal"]
        )

    )


    content.append(

        Paragraph(
            f"Budget: ₹{trip.budget}",
            styles["Normal"]
        )

    )


    content.append(

        Paragraph(
            f"Friends: {trip.friends}",
            styles["Normal"]
        )

    )


    content.append(

        Paragraph(
            f"Duration: {trip.duration}",
            styles["Normal"]
        )

    )


    content.append(Spacer(1,20))


    content.append(

        Paragraph(
            trip.plan.replace("\n","<br/>"),
            styles["Normal"]
        )

    )


    doc.build(content)


    pdf.seek(0)


    return send_file(

        pdf,

        as_attachment=True,

        download_name="Hangout_Trip_Plan.pdf",

        mimetype="application/pdf"

    )



# ---------------- DOWNLOAD CURRENT GENERATED PLAN PDF ----------------


@app.route("/download-pdf", methods=["POST"])
def download_pdf():


    plan_text = request.form.get("plan")


    if not plan_text:

        return "No plan available"



    pdf = io.BytesIO()


    doc = SimpleDocTemplate(pdf)


    styles = getSampleStyleSheet()


    content = []


    content.append(

        Paragraph(
            "AI Generated Trip Plan",
            styles["Title"]
        )

    )


    content.append(Spacer(1,20))


    content.append(

        Paragraph(
            plan_text.replace("\n","<br/>"),
            styles["Normal"]
        )

    )


    doc.build(content)


    pdf.seek(0)


    return send_file(

        pdf,

        as_attachment=True,

        download_name="Trip_Plan.pdf",

        mimetype="application/pdf"

    )

# ---------------- WEATHER API ----------------

# ---------------- WEATHER API ----------------

@app.route("/weather/<city>")
def weather(city):

    API_KEY = "0d5381376e0a536f6bb811dfebc1f3bf"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    print(response.text)   # ADD THIS FOR DEBUG


    if response.status_code != 200:

       return {
        "error": response.text
    }


    data = response.json()


    return {

        "city": data["name"],

        "temperature": data["main"]["temp"],

        "condition": data["weather"][0]["description"],

        "humidity": data["main"]["humidity"]

    }
# ---------------- RUN ----------------


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000)