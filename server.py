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

# Connect DB
db_connect = create_engine('sqlite:///moons.db')
# Initialise Flask app
app = Flask(__name__, static_url_path='')
# Initialise Alexa endpoint
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
# Initialise API stuff
api = Api(app)

# Helper: choose a sound based on the moon_type
def choose_sfx(x):
    return {
            1: "https://young-sierra-60676.herokuapp.com/moonget",
            2: "https://young-sierra-60676.herokuapp.com/bigmoonget",
            3: "https://young-sierra-60676.herokuapp.com/multimoonget",
            4: "https://young-sierra-60676.herokuapp.com/starget",
            }.get(x, "https://young-sierra-60676.herokuapp.com/moonget")

def gen_moon():
    conn = db_connect.connect()
    count = conn.execute("select Count(*) from moons").fetchone()[0]
    moon_id = randint(1,count)
    query = conn.execute("select * from moons where id =%d "  %int(moon_id))
    result = query.fetchone()
    template = "You got a moon! " + result['name']
    sfx = choose_sfx(result['moon_type'])
    location = result['kingdom']
    postgame = result['is_postgame']
    return [template, sfx, location, postgame]

def get_moon_alexa():
    moon = gen_moon()
    print("MOON:", moon)
    print("audio("+ moon[0]+ ").play("+moon[1]+")")
    return audio(moon[0]).play(moon[1]).simple_card(title='You Got A Moon!', content=moon[0]+'\nThis'+(' post-game ', '')[moon[3]]+ 'moon can be found in the '+moon[2]+' Kingdom.')

@ask.launch
def launch_moon():
    moon = gen_moon()
    return audio(moon[0]).play(moon[1]).simple_card(title='You Got A Moon!', content=moon[0]+'\nThis'+('',' post-game ')[moon[3]]+ 'moon can be found in the '+moon[2]+' Kingdom.')

@ask.intent('MoonIntent')
def intent_moon():
    moon = gen_moon()
    return audio(moon[0]).play(moon[1]).simple_card(title='You Got A Moon!', content=moon[0]+'\nThis moon can be found in the '+moon[2]+' Kingdom.')

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

@app.route('/starget')
def multimoonget():
    return app.send_static_file('starget.mp3')

api.add_resource(Moons, '/') # Route_1
api.add_resource(RandomMoon, '/random') # Route_2

# Init Flask etc.
if __name__ == '__main__':
    app.run(port=os.getenv('PORT', '5000'), host='0.0.0.0')
    # Init Discord bot
