from dotenv import load_dotenv
import os

load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    OPENWEATHER_API_KEY = os.getenv(
        "OPENWEATHER_API_KEY"
    )

    MAIL_USERNAME = os.getenv(
        "MAIL_USERNAME"
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD"
    )

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///weather.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False