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
            5: "https://young-sierra-60676.herokuapp.com/8bitmoonget",
            }.get(x, "https://young-sierra-60676.herokuapp.com/moonget")

def search_moon(query):
    conn = db_connect.connect()
    # count = conn.execute("select Count(*) from moons").fetchone()[0]
    # moon_id = randint(1,count)
    query = conn.execute("select * from moons where kingdom=% ORDER BY RAND() LIMIT 1 "  %str(query))
    result = query.fetchone()
    return gen_moon(result)

def random_moon():
    conn = db_connect.connect()
    count = conn.execute("select Count(*) from moons").fetchone()[0]
    moon_id = randint(1,count)
    query = conn.execute("select * from moons where id =%d "  %int(moon_id))
    result = query.fetchone()
    return gen_moon(result)

def gen_moon(record):
    sfx = choose_sfx(record['moon_type'])
    location = record['kingdom']
    postgame = record['is_postgame'] == "True"
    template = "Let's find a moon! " + record['name'] + ". Try searching for this moon in the " + location + " Kingdom" + (" after you've beaten the game.", ".")[postgame]
    return [template, sfx, location, postgame]

def get_moon_alexa():
    moon = random_moon()
    print("MOON:", moon)
    print("audio("+ moon[0]+ ").play("+moon[1]+")")
    return audio(moon[0]).play(moon[1]).simple_card(title='Let\'s Find A Moon!', content=moon[0])

@ask.launch
def launch_moon():
    moon = random_moon()
    return audio(moon[0]).play(moon[1]).simple_card(title='Let\'s Find A Moon!', content=moon[0]+'\nThis'+('',' post-game ')[moon[3]]+ 'moon can be found in the '+moon[2]+' Kingdom.')

@ask.intent('MoonIntent')
def intent_moon():
    moon = random_moon()
    return audio(moon[0]).play(moon[1]).simple_card(title='Let\'s Find A Moon!', content=moon[0]+'\nThis moon can be found in the '+moon[2]+' Kingdom.')

@ask.intent('KingdomMoonIntent', mapping={'kingdom': 'Kingdom'}, default={'kingdom':'Cap'})
def intent_search_moon(kingdom):
    moon = search_moon(kingdom)
    return audio(moon[0]).play(moon[1]).simple_card(title='Let\'s Find A Moon in the {} Kingdom!'.format(kingdom), content=moon[0])

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
def starget():
    return app.send_static_file('starget.mp3')

@app.route('/8bitmoonget')
def ebitmoonget():
    return app.send_static_file('8bitmoonget.mp3')

api.add_resource(Moons, '/') # Route_1
api.add_resource(RandomMoon, '/random') # Route_2

# Init Flask etc.
if __name__ == '__main__':
    app.run(port=os.getenv('PORT', '5000'), host='0.0.0.0')
    # Init Discord bot
