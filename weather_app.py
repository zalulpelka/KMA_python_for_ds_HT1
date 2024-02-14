import datetime as dt
import json

import requests
from flask import Flask, jsonify, request

# create your API token, and set it up in Postman collection as part of the Body section
API_TOKEN = "zalulpelka"
# you can get API keys for free here - https://api-ninjas.com/api/jokes
RSA_KEY = "8DFMHXR6J4F83QUDRGDHDVRQ7"

app = Flask(__name__)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


def get_weather(location: str, date1: str):
    url_base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

    url = f"{url_base_url}/{location}/{date1}?include=days&key={RSA_KEY}"
    
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    else:
        raise InvalidUsage(response.text, status_code=response.status_code)

def clean_data(response_json):
    weather_data = response_json.get("days")
    for data in weather_data:
        description = data["description"] 
        temp_f = data["temp"]
        humidity = data["humidity"]
        sunset_str = data["sunset"]
        sunrise_str = data["sunrise"]
        pressure = data["pressure"]
        windspeed = data["windspeed"]
        
    # f -> c
    temp_c = (temp_f - 32)*5/9
    temp_c = round(temp_c)

    # calculating daytime
    sunrise = dt.datetime.strptime(sunrise_str, "%H:%M:%S")
    sunset = dt.datetime.strptime(sunset_str, "%H:%M:%S")
    daytime = sunset - sunrise
    daytime = str(daytime)

    # mixmix
    result = {
        "desription": description,
        "temp_c": temp_c,
        "humidity" : humidity,
        "sunrise" : sunrise_str,
        "sunset" : sunset_str, 
        "daytime": daytime,
        "pressure": pressure,
        "windspeed": windspeed
    }

    return result
    
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p><h2>KMA L2: python Saas.</h2></p>"


@app.route("/content/api/v1/integration/generate", methods=["POST"])
def weather_endpoint():
    json_data = request.get_json()

    if json_data.get("token") is None:
        raise InvalidUsage("token is required", status_code=400)

    token = json_data.get("token")

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    if json_data.get("location") and json_data.get("date1") and json_data.get("requester_name"):
        requester_name = json_data.get("requester_name")
        location = json_data.get("location")
        date1 = json_data.get("date1")

    response = get_weather(location, date1)
    weather = clean_data(response)

    result = {
        "requester_name": requester_name,
        "date" : date1,
        "location": location,
        "weather": weather
    }

    return result
