from flask import Flask, g, render_template, jsonify
import json
from sqlalchemy import create_engine, text

USER = "root"
PASSWORD = "Onedirection1!" 
PORT = "3306"
DB = "dublin_bikes"
URI = "localhost"

app = Flask(__name__, static_url_path='') # tell Flask where are the static files (html, js, images, css, etc.)

#connect to data base 
def connect_to_db():
    connection_string = f"mysql+mysqldb://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}"
    engine = create_engine(connection_string, echo = True)
    
    return engine

# Create the engine variable and store it in the global Flask variable 'g'
def get_db():
    db_engine = getattr(g, '_database', None)
    if db_engine is None:
        db_engine = g._database = connect_to_db()
    return db_engine

# Show all stations in json
@app.route('/stations')
def get_stations():
    engine = get_db()
    
    stations = []
    rows = engine.connect().execute(text("SELECT * from station;")) # here station is the name of your table in the database
    
    for row in rows.mappings():
        stations.append(dict(row))
    
    return jsonify(stations=stations)

@app.route('/')
def root():
    return 'Navigate http://127.0.0.1:5000/stations'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)