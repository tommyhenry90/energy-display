import os
import pandas as pd
import pymongo
import json


def import_content(filepath, collection_name, usr="admin", pwd="admin"):
    data = pd.read_csv(filepath)
    data_json = json.loads(data.to_json(orient='records'))

    connection = pymongo.MongoClient("ds117540.mlab.com", 17540)
    db = connection["comp9321ass3"]
    db.authenticate(usr, pwd)
    collection = db[collection_name]
    collection.insert(data_json)

if __name__ == "__main__":
    filepath = 'elec_data.csv'
    import_content(filepath, "elec_data")