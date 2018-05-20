from mongoengine import connect
from model import EnergyReport, EnergySource
from PublicationService.data_objects import EnergyConsumption
import xml.etree.ElementTree as ET

def unggah():

    tree1 = ET.parse('dataset/consumption.xml')
    root1 = tree1.getroot()

    connect(
        db="comp9321ass3",
        username="admin",
        password="admin",
        host="ds117540.mlab.com",
        port=17540
    )
    # connect(
    #         db="db_01",
    #         username="user_01",
    #         password="abc123",
    #         host="ds040877.mlab.com",
    #         port=40877
    #     )
    EnergyConsumption.objects().delete()
    for record in root1.find('.//data'):
        country = record.find('.//field[1]').text
        year = record.find('.//field[3]').text
        try:
            amount = float(record.find('.//field[5]').text)
            raw = EnergyConsumption(country, year, amount)
            raw.save()
        except:
            amount = None
        print(country, year, amount)


if __name__ == "__main__":
    unggah()
