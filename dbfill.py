from sqlalchemy import create_engine
db_connect = create_engine('sqlite:///moons.db')
moonlist = open('moonlist', 'r')
for moon in moonlist:
    print([text.strip() for text in moon.split('|')])
    # conn = db_connect.connect()
    # count = conn.execute("select Count(*) from moons").fetchone()[0]
