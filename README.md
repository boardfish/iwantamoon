# The Odyssey

This project started out with me wanting to work with Amazon Alexa. I've owned
an Echo for quite some time, and after playing a bit of a sideline role back at
GreatUniHack 2016 with our Alexa project, I thought I'd learn to use it myself.

While many are done with Node.js, I chose to stick with Python for a little
familiarity. I needed to use the `flask-ask` suite to build my intents, which
pull from a locally-hosted database containing data for every Power Moon in
*Super Mario Odyssey*.

There are two different kinds of intent - one which throws you a random Moon
from throughout the game (836 are listed, counting the various Multi-Moons as
just one), and one that gives you a Moon from a Kingdom of your choice. While
Alexa doesn't play nicely with the latter, you can refer to Kingdoms either by
their theme ("the Snow Kingdom", "the Sand Kingdom") or their names ("Shiveria"
or "Tostarena" respectively).

Another two things that run on the server are an API that returns a random Moon
from the database, and a web frontend that gives you a random Moon from this
API. The idea there is to extend your experience with the game or challenge a
friend on your own terms to see who can find a particular Moon first. After
doing something similar with Kaze Emanuar's Net64 with a couple of friends at a
LAN, it's sure to be a blast.

There's also a Discord bot running on that API - perfect for the LAN scenario
above. Just type `!moon` in the chat and the bot will come running with a fresh
Moon and its Kingdom.

The web frontend takes a few hints from the game's menu screens for its own
styling, and I'm hoping for the skill to go live on the Alexa Skills Store with
any luck. As for the Discord bot, I'm going to see what I can do with it.
Hosting it on another Heroku dyno sounds alright.

## What I've Learned

I'm no stranger to Python at its most basic level - it was my first language -
but I never got much further with it than command-line inputs and outputs, aside
from a few forgettable hours dabbling with Tkinter. So learning Flask and how to
play with Alexa has really been something - it's been good to come home to my
first language while using it to its full extent. It surprised me just how good
it is for building an API - it makes a proper MVC solution like Rails look
bloated, which makes me very happy.

Python hasn't really been the focus, though - I've used this time to explore a
couple of things I've really wanted to learn for a while, those being Discord
bots and Alexa apps. It's not gone entirely swimmingly - I've hit hitches here
and there that have helped me understand both in bigger ways - but I'm glad to
say I think I've figured them out and I'll hopefully go on to make more. I don't
feel like I've got use out of a hackathon in this way for quite some time - by
playing it (relatively) safe, I've not only made something that's just about
good enough to use (I hope), but I've also given myself a decent education on
Flask, Alexa and Discord.
