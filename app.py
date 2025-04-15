from flask import Flask, jsonify, render_template, send_from_directory, make_response, request
from flask_cors import CORS
import requests
import os
import pickle
import numpy as np
import datetime
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Dublin"
COUNTRY_CODE = "IE"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY_CODE}&appid={WEATHER_API_KEY}&units=metric"

# Ensure both models are loaded correctly
bike_model = pickle.load(open('bike_availability_model_v1.pkl', 'rb'))
dock_model = pickle.load(open('bike_docks_model_v1.pkl', 'rb'))

# Add new prediction API endpoint
@app.route("/predict/<station_id>", methods=["GET"])
def predict_hourly(station_id):
    try:
        # Get the current date
        date = datetime.datetime.now()
        day_of_week = date.weekday()  # 0-6, 0 is Monday
        
        # Get weather data
        weather_data = get_weather_forecast()
        
        # Prepare prediction data for 24 hours
        hourly_predictions = []
        
        for hour in range(24):
            # Prepare features needed for prediction
            is_weekend = 1 if day_of_week >= 5 else 0
            is_rush_hour = 1 if (7 <= hour <= 9) or (17 <= hour <= 19) else 0
            
            features = [
                int(station_id),
                day_of_week,
                hour,
                weather_data['humidity'],
                weather_data['average_temperature'],
                is_weekend,
                is_rush_hour
            ]
            
            # Convert to numpy array for prediction
            input_array = np.array(features).reshape(1, -1)
            
            # Predict available bikes and docks using the correct model variable
            bike_prediction = max(0, int(bike_model.predict(input_array)[0]))  # Use bike_model
            dock_prediction = max(0, int(dock_model.predict(input_array)[0]))  # Use dock_model
            
            hourly_predictions.append({
                "hour": hour,
                "available_bikes": bike_prediction,
                "available_docks": dock_prediction
            })
        
        response = jsonify(hourly_predictions)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Functions for the prediction
def get_weather_forecast():
    '''Returns fixed weather data'''
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid={WEATHER_API_KEY}&units=metric")
    if response.status_code == 200:
        data = response.json()
        return {
            'average_temperature': (data['main']['temp_max']+data['main']['temp_min'])/2,
            'humidity': data['main']['humidity'],
        }
    else:
        print("Error fetching weather data")

def get_formatted_weather(city=CITY, country_code=COUNTRY_CODE):
    """Get weather data and format it for frontend display"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract relevant weather information
        weather_info = {
            "city": data['name'],
            "country": data['sys']['country'],
            "temperature": round(data['main']['temp']),
            "feels_like": round(data['main']['feels_like']),
            "description": data['weather'][0]['description'].capitalize(),
            "icon": data['weather'][0]['icon'],
            "humidity": data['main']['humidity'],
            "wind_speed": round(data['wind']['speed'] * 3.6, 1),  # Convert m/s to km/h
            "timestamp": datetime.datetime.now().strftime("%H:%M, %d %b %Y"),
        }
        
        return weather_info
    
    return None

# app = Flask(__name__, static_url_path='/static')

# Serve static media files
@app.route('/media/<path:filename>')
def media_files(filename):
    return send_from_directory('Media', filename)

# Main routes
@app.route("/")
def home():
    return render_template("index.html", google_maps_key=GOOGLE_MAPS_API_KEY)

@app.route("/homepage")
def homepage():
    '''Navigate to the homepage'''
    return render_template("homepage.html")

@app.route("/stations", methods=["GET"])
def get_bike_stations():
    '''fetches bike static bike station information from JCDecaux'''
    try:
        jcdecaux_api_key = os.getenv("BIKE_KEY")
        url = f"https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey={jcdecaux_api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch station data"}), 500

    except Exception as e:
        print(f"Error fetching JCDecaux data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/availability", methods=["GET"])
def get_station_availability():
    '''Fetches the availability for a specific station'''
    try:
        jcdecaux_api_key = os.getenv("BIKE_KEY")
        url = f"https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey={jcdecaux_api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            stations = response.json()
            availability_data = [
                {
                    "number": s["number"],
                    "available_bikes": s["available_bikes"],
                    "available_bike_stands": s["available_bike_stands"]
                }
                for s in stations
            ]
            return jsonify(availability_data)
        else:
            return jsonify({"error": "Failed to fetch availability data"}), 500

    except Exception as e:
        print(f"Error fetching availability data: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/weather", methods=["GET"])
def get_weather():
    '''Basic weather route (returns raw OpenWeatherMap data)'''
    response = requests.get(URL)
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Unable to retrieve weather data"}), 500


@app.route("/weather/formatted", methods=["GET"])
def get_formatted_weather_route():
    ''' Enhanced weather route with formatted data for frontend display'''
    city = request.args.get("city", CITY)
    country = request.args.get("country", COUNTRY_CODE)
    
    weather_data = get_formatted_weather(city, country)
    
    if weather_data:
        return jsonify(weather_data)
    return jsonify({"error": "Unable to retrieve weather data"}), 500

# Weather search route - allows searching for weather by location
@app.route("/weather/search", methods=["GET"])
def search_weather():
    '''weather search route - returns weather when location is entered'''
    location = request.args.get("location", "")
    
    if not location:
        return jsonify({"error": "Location parameter is required"}), 400
    
    # Default to Ireland if no country code provided
    if "," in location:
        city, country = location.split(",", 1)
        city = city.strip()
        country = country.strip()
    else:
        city = location.strip()
        country = COUNTRY_CODE
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={WEATHER_API_KEY}&units=metric"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = get_formatted_weather(city, country)
        return jsonify(weather_data)
    
    return jsonify({"error": f"Unable to find weather data for {location}"}), 404

# Ensure both models are loaded at the beginning
bike_model = pickle.load(open('bike_availability_model_v1.pkl', 'rb'))
dock_model = pickle.load(open('bike_docks_model_v1.pkl', 'rb'))

# Defining route for predictions
@app.route("/predict", methods=["GET"])
def predict():
    '''Predcition route for ML models'''
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
            # Prepare input features for both models
            input_features = [
                station_id,
                day_of_week,
                openweather_data['humidity'],
                openweather_data['average_temperature'],
            ]
            input_array = np.array(input_features).reshape(1, -1)
            
            # Predict available bikes using bike_model
            bike_prediction = bike_model.predict(input_array)
            
            # Predict available docks using dock_model
            dock_prediction = dock_model.predict(input_array)
            
            predictions[day_of_week] = {
                "available_bikes": int(bike_prediction[0]),
                "available_docks": int(dock_prediction[0])
            }
        
        response = jsonify({"predictions": predictions})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)