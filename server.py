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
    return [template, sfx]

def get_moon_alexa():
    moon = gen_moon()
    return audio(moon[0]).play(moon[1])

@ask.launch
def launch_moon():
    get_moon()

@ask.intent('MoonIntent')
def intent_moon():
    get_moon()

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

# Discord bot

mport discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, gen_moon()[0])
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

# Init Flask etc.
if __name__ == '__main__':
     app.run(port=os.getenv('PORT', '5000'), host='0.0.0.0')
# Init Discord bot
client.run(os.getenv('DISCORD_TOKEN', 'token'))
