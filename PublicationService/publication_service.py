from flask import Flask, jsonify
from flask_restful import reqparse
import requests
from mongoengine import StringField, IntField, FloatField, Document, \
    EmbeddedDocument, ListField, EmbeddedDocumentField, connect

import datetime

WEATHER_API_KEY = "5cbcafaa45789c29e8f91194dbe498be"
app = Flask(__name__)


@app.route("/weather", methods=["GET"])
def get_weather():
    parser = reqparse.RequestParser()
    parser.add_argument('city', type=str)
    parser.add_argument('country', type=str)

    args = parser.parse_args()

    city = args.get('city')
    country = args.get('country')

    location = city + ',' + country

    url = "https://api.openweathermap.org/data/2.5/weather"
    payload = {
        "q": location,
        "APPID": WEATHER_API_KEY
    }
    r = requests.get(url, params=payload)
    return jsonify(r.json()), 200


@app.route("/energy-mix", methods=["GET"])
def energy_mix():
    url = "http://data.un.org/Handlers/DataHandler.ashx?Service=query&Anchor=cmID%3aEL&Applied=&DataMartId=EDATA&UserQuery=Electricity&c=2,5,6,7,8&s=_crEngNameOrderBy:asc,_enID:asc,yr:desc&RequestId=26"


if __name__ == "__main__":
    app.run(debug=True)