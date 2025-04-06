from flask import Flask, jsonify, render_template, send_from_directory, make_response
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = "7226a2c4ce82265fde9c8d32f42258ec"
CITY = "Dublin"
COUNTRY_CODE = "IE"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY_CODE}&appid={API_KEY}&units=metric"

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

if __name__ == "__main__":
    app.run(debug=True)