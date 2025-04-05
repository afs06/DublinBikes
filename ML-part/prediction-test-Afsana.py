import pandas as pd
import pickle
from datetime import datetime
import requests

# Load the trained model
with open("bike_availability_model_v3.pkl", "rb") as file:
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
        

def predict_weekly_bike_availability(station_id):
    """Predict the number of available bikes for a chosen station for each day of the week"""
    # Use the function for weather forecast
    weather_features = get_weather_forecast()
    
    if weather_features['average_temperature'] is None or weather_features['humidity'] is None:
        return "Weather data unavailable. Cannot make predictions."

    predictions = {}
    
    for day_of_week in range(7):  # Loop through all days of the week (0=Monday, 6=Sunday)
        input_data = pd.DataFrame([{
            'station_id': station_id,
            'day_of_the_week': day_of_week,
            'humidity': weather_features['humidity'],
            'average_temperature': weather_features['average_temperature'],
        }])

        # Make prediction
        prediction = model.predict(input_data)
        predictions[day_of_week] = prediction[0]

    return predictions

# Example usage
station_id = 13

predicted_bikes = predict_weekly_bike_availability(station_id)
print(f"Predicted number of available bikes at station {station_id}: {predicted_bikes}")
