import requests
from config import Config

API_KEY = Config.OPENWEATHER_API_KEY


def get_weather(city):

    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    weather_response = requests.get(weather_url)

    weather_data = weather_response.json()

    if weather_response.status_code != 200:
        return None

    lat = weather_data["coord"]["lat"]
    lon = weather_data["coord"]["lon"]

    aqi_url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )

    aqi_response = requests.get(aqi_url)

    aqi_data = aqi_response.json()

    return {

        "temperature":
        weather_data["main"]["temp"],

        "humidity":
        weather_data["main"]["humidity"],

        "pressure":
        weather_data["main"]["pressure"],

        "wind_speed":
        weather_data["wind"]["speed"],

        "city":
        city,

        "aqi":
        aqi_data["list"][0]["main"]["aqi"]
    }