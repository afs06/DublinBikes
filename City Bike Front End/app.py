from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from the frontend

API_KEY = "7226a2c4ce82265fde9c8d32f42258ec"
CITY = "Dublin"
COUNTRY_CODE = "IE"  # Explicitly set country code to "IE" for Ireland
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY_CODE}&appid={API_KEY}&units=metric"

@app.route("/weather", methods=["GET"])
def get_weather():
    response = requests.get(URL)
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Unable to retrieve weather data"}), 500

if __name__ == "__main__":
    app.run(debug=True)