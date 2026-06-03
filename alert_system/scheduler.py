from models import WeatherAlert
from email_service import send_alert_email
from models import db


def alert_exists(
    user_id,
    alert_type
):

    return WeatherAlert.query.filter_by(
        user_id=user_id,
        alert_type=alert_type,
        status="ACTIVE"
    ).first()


def create_alert(
    app,
    user,
    alert_type,
    subject,
    body
):

    existing = alert_exists(
        user.id,
        alert_type
    )

    if existing:
        return

    send_alert_email(
        app,
        user.email,
        user.city,
        subject,
        body
    )

    alert = WeatherAlert(
        user_id=user.id,
        alert_type=alert_type
    )

    db.session.add(alert)
    db.session.commit()


from apscheduler.schedulers.background import BackgroundScheduler

from models import User
from models import db

from weather_service import get_weather

from alert_service import create_alert


def monitor_weather(app):

    with app.app_context():

        users = User.query.all()

        for user in users:

            weather = get_weather(
                user.city
            )

            if not weather:
                continue

            # Heat Wave

            if weather["temperature"] >= 42:

                create_alert(

                    app,

                    user,

                    "HEATWAVE",

                    "⚠ Heat Wave Alert",

                    f"""
Current Temperature:
{weather['temperature']}°C

Risk:
Heat stroke and dehydration.

Stay hydrated.
"""
                )

            # AQI

            if weather["aqi"] >= 4:

                create_alert(

                    app,

                    user,

                    "AQI",

                    "⚠ Air Quality Alert",

                    f"""
Current AQI:
{weather['aqi']}

Air quality is dangerous.

Avoid outdoor activities.
"""
                )

            # Storm

            if weather["wind_speed"] >= 15:

                create_alert(

                    app,

                    user,

                    "STORM",

                    "⚠ Storm Warning",

                    f"""
Wind Speed:
{weather['wind_speed']} m/s

Strong winds detected.

Stay indoors.
"""
                )


def start_scheduler(app):

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        func=lambda: monitor_weather(app),
        trigger="interval",
        minutes=30
    )

    scheduler.start()

#def monitor_weather(app):

 #   print("Scheduler Running...")

  #  with app.app_context():

   #     users = User.query.all()

    #    print("Users Found:", len(users))

     #   for user in users:

      #      print("Checking:", user.email)

       #     weather = get_weather(user.city)

        #    print(weather)