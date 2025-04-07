from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle
import requests
import datetime
import joblib
import os

app = Flask(__name__)

# Check if model file exists before loading
model = None
model_path_joblib = 'bike_availability_model_v1.joblib'
model_path_pkl = 'bike_availability_model_v1.pkl'

if os.path.exists(model_path_joblib):
    try:
        model = joblib.load(model_path_joblib)
        print(f"Model loaded from {model_path_joblib}")
    except Exception as e:
        print(f"Error loading joblib model: {e}")
elif os.path.exists(model_path_pkl):
    try:
        with open(model_path_pkl, 'rb') as f:
            model = pickle.load(f)
        print(f"Model loaded from {model_path_pkl}")
    except Exception as e:
        print(f"Error loading pickle model: {e}")
else:
    print("Warning: Model file not found. Using dummy predictions.")

# Function to get current weather data
def get_weather_forecast():
    '''Returns current weather data for Dublin'''
    try:
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Dublin&appid=7226a2c4ce82265fde9c8d32f42258ec&units=metric")
        if response.status_code == 200:
            data = response.json()
            return {
                'average_temperature': (data['main']['temp_max']+data['main']['temp_min'])/2,
                'humidity': data['main']['humidity'],
            }
        else:
            print(f"Error fetching weather data: Status {response.status_code}")
            return default_weather()
    except Exception as e:
        print(f"Exception while fetching weather data: {e}")
        return default_weather()

def default_weather():
    # Return default values if API call fails
    return {
        'average_temperature': 15,
        'humidity': 70,
    }

# Route for the home page
@app.route('/')
def home():
    # Get list of station IDs (assuming you have this information)
    # For demonstration, creating a sample list
    station_ids = list(range(1, 21))  # Stations 1-20
    return render_template('index.html', station_ids=station_ids)

# API endpoint to get predictions for a specific station
@app.route('/predict/<int:station_id>')
def predict(station_id):
    try:
        # Get current date and weather
        current_date = datetime.datetime.now()
        weather_data = get_weather_forecast()
        
        # Prepare prediction data for all hours of the day
        predictions = []
        
        for hour in range(24):
            # Create timestamp for the prediction hour
            prediction_time = current_date.replace(hour=hour, minute=0, second=0, microsecond=0)
            
            # Extract day of week (1=Monday, 7=Sunday)
            day_of_week = prediction_time.isoweekday()
            
            # Calculate is_weekend
            is_weekend = 1 if day_of_week >= 6 else 0
            
            # Calculate is_rush_hour
            is_rush_hour = 1 if hour in [7, 8, 17, 18] else 0
            
            # Create feature array for prediction
            features = [
                station_id,
                day_of_week,
                hour,
                weather_data['humidity'],
                weather_data['average_temperature'],
                is_weekend,
                is_rush_hour
            ]
            
            # Make prediction
            if model is not None:
                prediction = model.predict([features])[0]
                # Ensure prediction is non-negative and reasonable
                prediction = max(0, round(prediction, 1))
            else:
                # Dummy prediction if model failed to load
                prediction = 10 + hour % 10  # Simple pattern for testing
            
            predictions.append({
                'hour': hour,
                'predicted_bikes': prediction
            })
        
        return jsonify({
            'station_id': station_id,
            'date': current_date.strftime('%Y-%m-%d'),
            'weather': weather_data,
            'predictions': predictions
        })
    except Exception as e:
        print(f"Error in predict route: {e}")
        # Return a proper JSON error response instead of a 500 HTML page
        return jsonify({'error': f"Prediction failed: {str(e)}"}), 500

# Add a debug route to verify the application is working
@app.route('/debug')
def debug():
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None,
        'weather_working': get_weather_forecast() is not None
    })

if __name__ == '__main__':
    app.run(debug=True)