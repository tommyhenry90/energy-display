from mongoengine import StringField, IntField, FloatField, Document, \
    EmbeddedDocument, ListField, EmbeddedDocumentField, connect


class EnergyMix(Document):
    country = StringField(required=True)
    total_energy = FloatField(required=True)
    combustibles = FloatField(required=True)
    geothermal = FloatField(required=True)
    hydro = FloatField(required=True)
    solar = FloatField(required=True)
    wind = FloatField(required=True)
    year = IntField(required=True)

    def __init__(self, country, total_energy, combustibles, geothermal, hydro, solar, wind, year, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country = country
        self.total_energy = total_energy
        self.combustibles = combustibles
        self.geothermal = geothermal
        self.hydro = hydro
        self.solar = solar
        self.wind = wind
        self.year = year
