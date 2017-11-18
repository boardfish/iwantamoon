from sqlalchemy import create_engine, text
db_connect = create_engine('sqlite:///moons.db')
moonlist = open('moonlist', 'r')
conn = db_connect.connect()
statement = text("""INSERT INTO moons (kingdom, name, moon_type, is_postgame) VALUES (:kingdom, :name, :moon_type, :is_postgame)""") 
for moon in moonlist:
    moon_data = [text.strip() for text in moon.split('|')]
    data = ( { "kingdom": moon_data[0], "name": moon_data[1], "moon_type": moon_data[3], "is_postgame": moon_data[2] } )
    conn.execute(statement, **data)
    print("Added", data['name'])

