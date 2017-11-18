#!/usr/bin/env python
import logging
from flask import Flask, request
from flask_restful import Resource, Api
from flask_ask import Ask, statement, question, session, audio
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
from random import randint
import os

db_connect = create_engine('sqlite:///moons.db')
app = Flask(__name__, static_url_path='')
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
api = Api(app)

def choose_sfx(x):
    return {
            1: "https://young-sierra-60676.herokuapp.com/moonget",
            2: "https://young-sierra-60676.herokuapp.com/bigmoonget",
            3: "https://young-sierra-60676.herokuapp.com/multimoonget",
            4: "https://young-sierra-60676.herokuapp.com/starget",
            }.get(x, "https://young-sierra-60676.herokuapp.com/moonget")

@ask.launch
def launch_moon():
    conn = db_connect.connect()
    count = conn.execute("select Count(*) from moons").fetchone()[0]
    moon_id = randint(1,count)
    query = conn.execute("select * from moons where id =%d "  %int(moon_id))
    result = query.fetchone()
    template = "You got a moon! " + result['name']
    sfx = choose_sfx(int(result['moon_type']))
    return audio(template).play(sfx)

@ask.intent('MoonIntent')
def moon():
    conn = db_connect.connect()
    count = conn.execute("select Count(*) from moons").fetchone()[0]
    moon_id = randint(1,count)
    query = conn.execute("select name from moons where id =%d "  %int(moon_id))
    result = query.fetchone()[0]
    return audio("You got a moon! " + result).play("https://young-sierra-60676.herokuapp.com/moonget")

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
        
@app.route('/moonget')
def moonget():
    return app.send_static_file('moonget.mp3')

@app.route('/bigmoonget')
def bigmoonget():
    return app.send_static_file('bigmoonget.mp3')

@app.route('/multimoonget')
def multimoonget():
    return app.send_static_file('multimoonget.mp3')

api.add_resource(Moons, '/') # Route_1
api.add_resource(RandomMoon, '/random') # Route_2


if __name__ == '__main__':
     app.run(port=os.getenv('PORT', '5000'), host='0.0.0.0')
