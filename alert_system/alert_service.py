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