from flask import Flask, request, jsonify
from datetime import datetime
import numpy as np
import requests
import pickle
from flask_cors import CORS

modelname = "City Bike Front End/bike_availability_model_v3.pkl"
with open(modelname, "rb") as file:
    model = pickle.load(file)

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

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={
    r"/predict": {
        "origins": ["http://127.0.0.1:3000", "http://localhost:3000"],
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

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
        
        print("Sending predictions:", predictions, flush=True)
        response = jsonify({"predictions": predictions})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

        #return jsonify({"predictions": predictions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)