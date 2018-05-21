from flask import Flask, jsonify
from flask_restful import reqparse
import requests
from PublicationService.data_objects import EnergyMix, EnergyAccess, Population,EnergyConsumption
from mongoengine import connect
from importer import mix
from model import EnergyReport, EnergySource

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


@app.route("/energymix/<country>/<year>", methods=["GET"])
def energy_mix(country, year=2015):
    connect(
        db="comp9321ass3",
        username="admin",
        password="admin",
        host="ds117540.mlab.com",
        port=17540
    )

    mix = None
    for e in EnergyMix.objects(country=country, year=year):
        mix = e
    if not mix:
        response = jsonify(country=country, year=year)
        response.headers._list.append(('Access-Control-Allow-Origin', '*'))
        return response, 404
    energy_mix = {
        "country": country,
        "year": year,
        "total_energy": mix.total_energy,
        "combustibles": mix.combustibles,
        "geothermal": mix.geothermal,
        "hydro": mix.hydro,
        "nuclear": mix.nuclear,
        "solar": mix.solar,
        "wind": mix.wind,
        "other": mix.other
    }

    response = jsonify(energy_mix)
    response.headers._list.append(('Access-Control-Allow-Origin', '*'))
    return response, 200


@app.route("/energyaccess/<country>/<year>", methods=["GET"])
def energy_access(country, year):
    connect(
        db="comp9321ass3",
        username="admin",
        password="admin",
        host="ds117540.mlab.com",
        port=17540
    )

    access = None
    for e in EnergyAccess.objects(country=country, year=year):
        access = e
    if not access:
        response = jsonify(country=country, year=year)
        response.headers._list.append(('Access-Control-Allow-Origin', '*'))
        return response, 404

    energy_access = {
        "country": country,
        "year": year,
        "energy_access": access.energy_access
    }
    response = jsonify(energy_access)
    response.headers._list.append(('Access-Control-Allow-Origin', '*'))
    return response, 200


@app.route("/population/<country>/<year>", methods=["GET"])
def population(country, year):
    connect(
        db="comp9321ass3",
        username="admin",
        password="admin",
        host="ds117540.mlab.com",
        port=17540
    )

    pop = None
    for p in Population.objects(country=country, year=year):
        pop = p
    if not pop:
        response = jsonify(country=country, year=year)
        response.headers._list.append(('Access-Control-Allow-Origin', '*'))
        return response, 404

    population_response = {
        "country": country,
        "year": year,
        "population": pop.population
    }
    response = jsonify(population_response)
    response.headers._list.append(('Access-Control-Allow-Origin', '*'))
    return response, 200


@app.route("/consumption/<country>/<year>", methods=["GET"])
def consumption(country, year):
    connect(
        db="comp9321ass3",
        username="admin",
        password="admin",
        host="ds117540.mlab.com",
        port=17540
    )

    cons = None
    for p in EnergyConsumption.objects(country=country, year=year):
        cons = p
    if not cons:
        response = jsonify(country=country, year=year)
        response.headers._list.append(('Access-Control-Allow-Origin', '*'))
        return response, 404

    population_response = {
        "country": country,
        "year": year,
        "population": cons.energy_consumption
    }
    response = jsonify(population_response)
    response.headers._list.append(('Access-Control-Allow-Origin', '*'))
    return response, 200


@app.route("/reports/<country>/<year>", methods=["GET"])
def reports(country,year):
    connect(
        db="comp9321ass3",
        username="admin",
        password="admin",
        host="ds117540.mlab.com",
        port=17540
    )

    if not EnergyReport.object(country=country,year=year):
        mix(country, year)
    result = None
    for base in EnergyReport.objects(country=country,year=year):
        sources = list()

        for source in base.production_source:
            percent = round(source.amount/base.production_amount,2)
            sources.append({
                'type':source.energy_type,
                'amount': source.amount,
                'percent': percent
            })

        cons_per = base.consumption_amount / (base.population * base.energy_access / 100)

        year_next = year + 1
        year_prev = year - 1

        next_report = None
        prev_report = None

        if EnergyReport.object(country=country, year=year_next):
            next_report = "/".join('/reports', base.country, year_next)

        if EnergyReport.object(country=country, year=year_prev):
            prev_report = "/".join('/reports', base.country, year_prev)

        delta = base.production_amount - base.consumption_amount
        result = {
            "country": base.country,
            "year": base.year,
            "population": base.population,
            "energy_access": base.energy_access,
            "consumption": base.consumption_amount,
            "production": base.production_amount,
            "sources": sources,
            "delta_energy": delta,
            "consumption_percapita": cons_per,
            "link": {
                "prev": prev_report,
                "next": next_report
            }

        }
    if result is None:
        response = jsonify(result)
        response.headers._list.append(('Access-Control-Allow-Origin', '*'))
        return response, 200
    else:
        result = {
            "country": country,
            "year": year
        }
        response = jsonify(result)

        return response, 404


if __name__ == "__main__":
    app.run(debug=True, port=5001)
