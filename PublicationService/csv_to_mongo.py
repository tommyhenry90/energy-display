import pandas as pd
import pymongo
import json


def csv_to_json(filepath):
    data = pd.read_csv(filepath)
    json_data = json.loads(data.to_json(orient='records'))
    return json_data


def json_to_mongo(json_data, collection_name, usr="admin", pwd="admin"):
    connection = pymongo.MongoClient("ds117540.mlab.com", 17540)
    db = connection["comp9321ass3"]
    db.authenticate(usr, pwd)
    collection = db[collection_name]
    collection.insert(json_data)


if __name__ == "__main__":
    filepath = 'sunshine_data.csv'
    json_data = csv_to_json(filepath)
    json_to_mongo(json_data, "sunshine_data")