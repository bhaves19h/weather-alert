from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for
)

from weather_service import get_weather
from models import db, User, WeatherLog
from scheduler import start_scheduler
from email_service import mail
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from config import Config
from models import db, User

app = Flask(__name__)

app.config.from_object(Config)
mail.init_app(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():

    if "user_id" in session:
        return redirect("/dashboard")

    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        city = request.form["city"]

        password = generate_password_hash(
            request.form["password"]
        )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            return "Email already exists"

        user = User(
            username=username,
            email=email,
            city=city,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):
            session["user_id"] = user.id
            return redirect("/dashboard")

        return "Invalid Credentials"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    user = db.session.get(
        User,
        session["user_id"]
    )

    weather = get_weather(user.city)

    if weather:

        log = WeatherLog(
            city=weather["city"],
            temperature=weather["temperature"],
            humidity=weather["humidity"],
            wind_speed=weather["wind_speed"],
            pressure=weather["pressure"],
            aqi=weather["aqi"]
        )

        db.session.add(log)
        db.session.commit()

    history = (
        WeatherLog.query
        .order_by(
            WeatherLog.created_at.desc()
        )
        .limit(10)
        .all()
    )

    history.reverse()

    return render_template(
        "dashboard.html",
        user=user,
        weather=weather,
        history=history
    )

#@app.route("/test-email")
#def test_email():

 #   from email_service import send_alert_email

  #  send_alert_email(
   #     app,
    #    "b.07bhavesh@gmail.com",
     #   "Jaipur",
      #  "Test Alert",
       # "Weather Alert System is working."
    #)

    #return "Email Sent"

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

start_scheduler(app)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from scheduler import monitor_weather

with app.app_context():
    monitor_weather(app)


