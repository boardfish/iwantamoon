#!/usr/bin/env python
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
from random import randint
import os

db_connect = create_engine('sqlite:///moons.db')
app = Flask(__name__)
api = Api(app)

class Moons(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select id, name, kingdom from moons;")
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class RandomMoon(Resource):
    def get(self):
        conn = db_connect.connect()
        count = conn.execute("select Count(*) from moons").fetchone()[0]
        moon_id = randint(1,count)
        query = conn.execute("select * from moons where id =%d "  %int(moon_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
        

api.add_resource(Moons, '/') # Route_1
api.add_resource(RandomMoon, '/random') # Route_2


if __name__ == '__main__':
     app.run(port=os.getenv('PORT', '5002'), host='0.0.0.0')
