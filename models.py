from datetime import datetime
import os
from ponyorm.orm import Database, Required

db = Database('sqlite', os.path.join(os.getcwd(), 'divvy.sqlite'))

class Station(db.Entity):
    name = Required(unicode)
    divvy_id = Required(int)
    latitude = Required(float)
    longitude = Required(float)
    street_address = Required(unicode)
    location = Required(unicode)
    city = Required(unicode)
    zip_code = Required(unicode)
    total_docks = Required(int)
    last_updated = Required(datetime)


def database_cursor(create_tables=False):
    conn = sqlite3.connect('divvy_stations.sqlite')
    cursor = conn.cursor()
    if create_tables:
        cursor.execute('''
                CREATE TABLE stations
                (id integer, latitude real, longitude real, name text, 
                street_address text, location text, city text, zip_code text, 
                total_docks integer, last_updated timestamp)
                ''')
    return cursor 

def station_by_name(station_name):
    cursor = database_cursor()
    cursor.execute('''
        SELECT *
          FROM stations
         WHERE name like ?
         ''', station_name)
    return cursor.fetchall()

def all_stations():
    cursor = database_cursor()
    cursor.execute('''
        SELECT *
          FROM stations
          ''')
    return cursor.fetchall()

def update_station(station):

