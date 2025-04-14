###-----ALL relevant bike station information-----####
#import dbinfo
import requests
import json
import datetime
import time
import os
import traceback
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
JCKEY = os.getenv("BIKE_KEY")
Contract_NAME = "dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

#Fetch data from JCDeaux API
r = requests.get(STATIONS_URI, params={"apiKey":JCKEY,"contract":Contract_NAME})

#test loading json data
data = json.loads(r.text)

#print(json.dumps(data, indent=4))

#Downloading + Save Json data to a file
def write_to_file(text):
   
    # create folder in directory    
    if not os.path.exists('data'):
        os.mkdir('data')
        print("Folder 'data' created!")
    else:
        print("Folder 'data' already exists.")

    # now is a variable from datetime, which will go in {}.
    # replace is replacing white spaces with underscores in the file names
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"data/bikes_{now}.json"
    with open(filename, "w") as f:
        f.write(text)


# extract station details
def stations_to_db(text):
    #load the stations from the text received from jcdecaux
    stations = json.loads(text)

    # print type of the stations object, and number of stations
    print(type(stations), len(stations))
    
    # print the stations and load the content
    for station in stations:
        print(station)
        
        # extract the relevant info from the dictionary for static data
        vals = (station.get('address'), 
                station.get('number'),
                station.get('position').get('lat'),
                station.get('position').get('lng'),
                int(station.get('banking')), 
                int(station.get('bike_stands')), 
                station.get('name'), 
                station.get('status'),
                station.get('available_bike_stands'), 
                station.get('available_bikes'),
                )
        print(vals)

#----connect to the database ----
USER = "root" #add the according root from Joy
PASSWORD = "...."
PORT = "3306"
DB = "local_databasejcdecaux"
URI = "127.0.0.1" #add the EC2 Link from AWS

connection_string = f"mysql+pymysql://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}"

engine = create_engine(connection_string, echo = True)

#create station table
sql_stations = ''' 
CREATE TABLE IF NOT EXISTS station (
number INTEGER PRIMARY KEY,
address VARCHAR(256), 
banking INTEGER,
bikestands INTEGER,
name VARCHAR(256),
status VARCHAR(256)),
position_lat FLOAT,
position_lng FLOAT,
available_bike_stands INT,
'''
# Use the engine to execute the DESCRIBE command to inspect the table schema
#tab_structure = engine.execute("SHOW COLUMNS FROM station;")

# Fetch and print the result to see the columns of the table
#columns = tab_structure.fetchall()
#print(columns)

#CREATE AVAILABILITY TABLE
sql_availability = """
CREATE TABLE IF NOT EXISTS availability (
number INTEGER,
available_bikes INTEGER,
available_bike_stands INTEGER,
last_update DATETIME,
PRIMARY KEY (number, last_update)
);
"""

# Execute the query
engine.execute(sql_stations)
engine.execute(sql_availability)

#insert station data into database
def insert_station_data(station):
    sql = """
    INSERT INTO station (number, address, banking, bike_stands, name, position_lat, position_lng)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    address = VALUES(address), banking = VALUES(banking),
    bike_stands = VALUES(bike_stands), name = VALUES(name),
    position_lat = VALUES(position_lat), position_lng = VALUES(position_lng);
    """
    
    values = (
        station['number'],
        station['address'],
        int(station['banking']),
        int(station['bike_stands']),
        station['name'],
        station['position']['lat'],
        station['position']['lng']
    )

    with engine.connect() as conn:
        conn.execute(sql, values)

def insert_availability_data(station):
    sql = """
    INSERT INTO availability (number, available_bikes, available_bike_stands, last_update)
    VALUES (%s, %s, %s, %s);
    """
    
    values = (
        station['number'],
        station['available_bikes'],
        station['available_bike_stands'],
        datetime.utcfromtimestamp(station['last_update'] / 1000)  # Convert timestamp
    )

    with engine.connect() as conn:
        conn.execute(sql, values)

#Function to collect station  & availability data every 5 minutes into database
def main():
    while True:
        try:
            r = requests.get(STATIONS_URI, params={"apiKey": JCKEY, "contract": Contract_NAME})
            data = json.loads(r.text)

            # Save data locally
            write_to_file(json.dumps(data, indent=4))

            # Insert into DB
            for station in data:
                insert_station_data(station)  # Static data
                insert_availability_data(station)  # availability
            time.sleep(5 * 60)  # every 5 minutes # NOTE run on terminal $ nohup python get_jcdecaux.py )
        except: #if errors print traceback
            print(traceback.format_exc())

#Function to extract bike station data every 5min   
def station_data_frequently():
    while True:
        try:
            r = requests.get(STATIONS_URI, params={"apiKey": JCKEY, "contract": Contract_NAME})
            data = json.loads(r.text)

            # Save data locally
            write_to_file(json.dumps(data, indent=4))

            stations_to_db(r.text)
            time.sleep(5 * 60)  # every 5 minutes # NOTE run on terminal $ nohup python get_jcdecaux.py )
        except: #if errors print traceback
            print(traceback.format_exc())

# CTRL + Z or CTRL + C to stop it
#station_data_frequently()




