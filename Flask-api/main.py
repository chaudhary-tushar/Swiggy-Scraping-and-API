from flask import Flask,jsonify
import pymongo
import sys
import json
from bson import json_util
app = Flask(__name__)

####connecting to server######
try:
    mongo=pymongo.MongoClient(
        host="localhost",
        port=27017 
    )
    db=mongo.swiggdb
    
except:
    print("Cannot connect to MongDB")
    sys.exit()


@app.route('/cities',methods=['GET'])
def list_cities():
    data=db.Cities.find()
    json_data = json_util.dumps(data)
    return jsonify(json.loads(json_data))
    
@app.route('/restaurants',methods=['GET'])
def list_restaurants():
    data=db.Restaurants.find().limit(100)
    json_data = json_util.dumps(data)
    return jsonify(json.loads(json_data))

@app.route('/topres/<string:city_name>',methods=['GET'])
def topres(city_name):
    city_name=city_name.capitalize()
    data=db.Restaurants.find({ "City": f"{city_name}" })
    data = sorted(data, key=lambda x: float(x["Ratings"]), reverse=True)[:10]
    json_data = json_util.dumps(data)
    return jsonify(json.loads(json_data))

if __name__=="__main__":
    app.run(debug=True)