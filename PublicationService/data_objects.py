from mongoengine import StringField, IntField, FloatField, Document, \
    EmbeddedDocument, ListField, EmbeddedDocumentField, connect
from PublicationService.csv_to_mongo import *


class EnergyMix(Document):
    country = StringField(required=True)
    year = IntField(required=True)
    total_energy = FloatField(required=True)
    combustibles = FloatField(required=False)
    geothermal = FloatField(required=False)
    hydro = FloatField(required=False)
    solar = FloatField(required=False)
    wind = FloatField(required=False)
    nuclear = FloatField(required=False)

    def __init__(self, country, total_energy, combustibles, geothermal, hydro, solar, wind, year, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country = country
        self.year = year
        self.total_energy = total_energy
        self.combustibles = combustibles
        self.geothermal = geothermal
        self.hydro = hydro
        self.solar = solar
        self.wind = wind

    def add_element(self, energy_type, amount):
        if energy_type == "total_energy":
            self.total_energy = amount
        elif energy_type == "combustibles":
            self.combustibles = amount
        elif energy_type == "geothermal":
            self.geothermal = amount
        elif energy_type == "hydro":
            self.hydro = amount
        elif energy_type == "nuclear":
            self.nuclear = amount
        elif energy_type == "solar":
            self.solar = amount
        elif energy_type == "wind":
            self.wind = amount

    def add_new_element(self, keyword, argument):
        setattr(self, keyword, argument)


class EnergyAccess(Document):
    country = StringField(required=True)
    year = IntField(required=True)
    energy_access = FloatField(required=True)

    def __init__(self, country, year, energy_access, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country = country
        self.year = year
        self.energy_access = energy_access


class Population(Document):
    country = StringField(required=True)
    year = IntField(required=True)
    population = IntField(required=True)

    def __int__(self, country, year, population, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country = country
        self.year = year
        self.population = population


class CSVStructure:
    def __init__(self):
        self.total_energy = "Electricity - Gross production"
        self.combustibles = "From combustible fuels – Main activity"
        self.geothermal = "Geothermal – Main activity"
        self.hydro = "Hydro – Main activity"
        self.nuclear = "Nuclear – Main activity"
        self.other = "From other sources – Main activity"
        self.solar = "Solar – Main activity"
        self.wind = "Wind – Main activity"
        self.combustibles2 = "From combustible fuels – Autoproducer"
        self.hydro2 = "Hydro – Autoproducer"
        self.other2 = "From other sources – Autoproducer"
        self.solar2 = "Solar – Autoproducer"
        self.wind2 = "Wind – Autoproducer"
        self.losses = "Electricity - Losses"


ENERGY_CATEGORIES = {
    "Electricity - Gross production": "total_energy",
    "From combustible fuels – Main activity": "combustibles",
    "Geothermal – Main activity":"geothermal",
    "Hydro – Main activity":"hydro",
    "Nuclear – Main activity":"nuclear",
    "From other sources – Main activity":"other",
    "Solar – Main activity":"solar",
    "Wind – Main activity":"wind",
    "From combustible fuels – Autoproducer":"combustibles2",
    "Geothermal – Autoproducer":"geothermal2",
    "Hydro – Autoproducer":"hydro2",
    "Nuclear - Autoproducer":"nuclear2",
    "From other sources – Autoproducer":"other2",
    "Solar – Autoproducer":"solar2",
    "Wind – Autoproducer":"wind2",
}

database = []


def process_csv(data_input):
    for entry in data_input:
        energy_type = entry["Commodity - Transaction"]
        if energy_type in ENERGY_CATEGORIES:
            energy_category = ENERGY_CATEGORIES[energy_type]
            country = entry["Country or Area"]
            year = entry["Year"]
            amount = entry["Quantity"]
            exists = False
            for mix in database:
                if mix.country == country and mix.year == year:
                    setattr(mix, energy_category, amount)
                    exists = True
                    break
            if not exists:
                mix = EnergyMix
                mix.country = country
                mix.year = year
                setattr(mix, energy_category, amount)
                database.append(mix)


if __name__ == '__main__':
    data = csv_to_json("data.csv")
    process_csv(data)
    for i in database:
        print(i.country, i.solar)