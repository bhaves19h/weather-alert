from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    city = db.Column(
        db.String(100),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class WeatherLog(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    city = db.Column(
        db.String(100)
    )

    temperature = db.Column(
        db.Float
    )

    humidity = db.Column(
        db.Integer
    )

    wind_speed = db.Column(
        db.Float
    )

    pressure = db.Column(
        db.Integer
    )

    aqi = db.Column(
        db.Integer
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class WeatherAlert(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    alert_type = db.Column(
        db.String(50),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="ACTIVE"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

