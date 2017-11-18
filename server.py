#!/usr/bin/env python
import logging
from flask import Flask, request
from flask_restful import Resource, Api
from flask_ask import Ask, statement, question, session
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
from random import randint
import os

db_connect = create_engine('sqlite:///moons.db')
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
api = Api(app)

@ask.launch

@ask.intent('MoonIntent')
def moon():
    conn = db_connect.connect()
    count = conn.execute("select Count(*) from moons").fetchone()[0]
    moon_id = randint(1,count)
    query = conn.execute("select name from moons where id =%d "  %int(moon_id))
    result = query.fetchone()[0]
    return statement("You got a moon! " + result)

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
     app.run(port=os.getenv('PORT', '5000'), host='0.0.0.0')
