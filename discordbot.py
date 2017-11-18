import os
import discord
import asyncio
from sqlalchemy import create_engine
from random import randint

db_connect = create_engine('sqlite:///moons.db')
# Discord bot

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
    template = "__**Let's find a moon!**__\n__" + result['name'] + "__\nYou can find this moon in the **" + result['kingdom'] + " Kingdom**" + ("post-game.", ".")[result['is_postgame']]
    sfx = choose_sfx(result['moon_type'])
    return [template, sfx]

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!moon'):
        tmp = await client.send_message(message.channel, gen_moon()[0])
    elif message.content.startswith('!credits'):
        await client.send_message(message.channel, 'This bot is by **boardfish**, made during BrumHacks 7.0.')

client.run(os.getenv('DISCORD_TOKEN', 'token'))
