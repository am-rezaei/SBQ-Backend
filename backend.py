from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime

app = Flask(__name__)
CORS(app, support_credentials=True)

client = MongoClient('localhost',
                     username='admin',
                     password='@aA12345678')

db = client.admin


@app.route('/add', methods=['POST'])
@cross_origin(supports_credentials=True)
def add():
    inserted = db.data.insert_one(
        {
            "lat": request.json['lat']
            , "lng": request.json['lng']
            , "type": request.json['type']
            , "value": request.json['value']
            , "timestamp": datetime.now()
        })
    return str(inserted.inserted_id)


@app.route('/getAll')
@cross_origin(supports_credentials=True)
def get_all():
    collection = db['data']
    cursor = collection.find({})
    list_cur = list(cursor)
    return dumps(list_cur);

@app.route('/getTitle')
@cross_origin(supports_credentials=True)
def getTitle():
    return "Magnetic Fields";

@app.route('/clearData')
@cross_origin(supports_credentials=True)
def clearData():
    db.data.delete_many({})
    return "ok";

@app.route('/health')
@cross_origin(supports_credentials=True)
def health_check():
    return 'Im Good, Thanks!!';


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
