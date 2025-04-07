from flask import Flask, jsonify, render_template, send_from_directory, make_response, request
from flask_cors import CORS
import requests
import os
import pickle
import requests
import numpy as np

app = Flask(__name__)
CORS(app)

API_KEY = "7226a2c4ce82265fde9c8d32f42258ec"
CITY = "Dublin"
COUNTRY_CODE = "IE"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY_CODE}&appid={API_KEY}&units=metric"

#open ML model
modelname = "ML-part/bike_availability_model_v3.pkl"
with open(modelname, "rb") as file:
    model = pickle.load(file)
#Functions for the prediction
def get_weather_forecast():
    '''Returns fixed weather fata'''
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid=7226a2c4ce82265fde9c8d32f42258ec&units=metric")
    if response.status_code == 200:
        data = response.json()
        return {
            'average_temperature': (data['main']['temp_max']+data['main']['temp_min'])/2,
            'humidity': data['main']['humidity'],
        }
    else:
        print("Error fetching weather data")

# Serve static media files
@app.route('/media/<path:filename>')
def media_files(filename):
    return send_from_directory('Media', filename)

# Main routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/weather", methods=["GET"])
def get_weather():
    response = requests.get(URL)
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Unable to retrieve weather data"}), 500

#Defining route for predictions
@app.route("/predict", methods=["GET"])
def predict():
    try:
        station_id = request.args.get("station_id")
        if not station_id:
            return jsonify({"error": "Missing station_id parameter"}), 400

        try:
            station_id = int(station_id)
        except ValueError:
            return jsonify({"error": "station_id must be an integer"}), 400

        openweather_data = get_weather_forecast()

        predictions = {}

        for day_of_week in range(7):
            input_features = [
                station_id,
                day_of_week,
                openweather_data['humidity'],
                openweather_data['average_temperature'],
            ]
            input_array = np.array(input_features).reshape(1, -1)
            prediction = model.predict(input_array)
            predictions[day_of_week] = int(prediction[0])
        
        response = jsonify({"predictions": predictions})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

        #return jsonify({"predictions": predictions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
