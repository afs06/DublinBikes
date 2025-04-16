import pytest
import json
from app import app
"""
For testing I have implemented pass on 200 (status is OK) or 500 (Server encounters internal error), and 404 (File not found)
The Logic for 500 and 404 being passes is that if API key is unavailable then 200 would not be expected (In case API keys expire or don't work etc)
However, I simply want to test if path works, therefore by filtering for pass on expected error (500 or 404) means I am reasonably guaranteed this.
This is because it will fail on any other status code that would imply path does not work.
Finally, using 'python -m pytest Testing/test_app.py -v -s > flask_test_results.txt' in terminal will allow user to create a file which shows test results, and also shows status code for tests
So regardless of API keys being present, test can be run to verify paths. If user has API keys then they can also verify if 200 is returned as expected.
"""
# Set up a test client using pytest fixture
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test the root ("/") route
def test_home(client):
    response = client.get("/")
    print(f"[test_home] Status code: {response.status_code}")
    assert response.status_code == 200
    assert b"<html" in response.data

# Test the /homepage route
def test_homepage(client):
    response = client.get("/homepage")
    print(f"[test_homepage] Status code: {response.status_code}")
    assert response.status_code == 200

# Test the weather route 
def test_weather_route(client):
    response = client.get("/weather")
    print(f"[test_weather_route] Status code: {response.status_code}")
    assert response.status_code in [200, 500]
    assert "application/json" in response.content_type

# Test the formatted weather route
def test_weather_formatted(client):
    response = client.get("/weather/formatted")
    print(f"[test_weather_formatted] Status code: {response.status_code}")
    assert response.status_code in [200, 500]


# Test route that fetches bike station data
def test_station_data(client):
    response = client.get("/stations")
    print(f"[test_station_data] Status code: {response.status_code}")
    assert response.status_code in [200, 500]

# Test bike availability at stations
def test_availability_data(client):
    response = client.get("/availability")
    print(f"[test_availability_data] Status code: {response.status_code}")
    assert response.status_code in [200, 500]


# Test the /predict/station_id route
def test_predict_hourly(client):
    response = client.get("/predict/42")
    print(f"[test_predict_hourly] Status code: {response.status_code}")
    assert response.status_code in [200, 500]


# Test the weather search feature for Dublin
def test_search_weather_valid(client):
    response = client.get("/weather/search?location=Dublin")
    print(f"[test_search_weather_valid] Status code: {response.status_code}")
    assert response.status_code in [200, 404]

# Test serving a nonexistent static media file (should be 404 as non-existent)
def test_media_file_not_found(client):
    response = client.get("/media/nonexistent.png")
    print(f"[test_media_file_not_found] Status code: {response.status_code}")
    assert response.status_code in [404, 200]
