import requests
import json

API_KEY = "7226a2c4ce82265fde9c8d32f42258ec"
CITY = "Dublin"
API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def get_weather():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    return None
