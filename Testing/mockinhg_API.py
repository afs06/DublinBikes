import unittest
import requests
import json
from unittest.mock import patch, Mock
import os
from dotenv import load_dotenv


load_dotenv()
JCKEY = "eeb44b00e16a123704765d0077479e41fe503728"
Contract_NAME = "dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"


WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Dublin"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"

#Functions to test API request
def get_station_info():
    '''Function to test API request from JCdecaux'''
    response = requests.get(STATIONS_URI, params={"apiKey":JCKEY,"contract":Contract_NAME})
    if response.status_code == 200:
        station_data = response.json()
        print (json.dumps(station_data, indent=4))
        return station_data
    else:
        print("Error fetching bike station data:", response.status_code)
        return None


def get_weather():
    '''Function to test API request from Openweather'''
    response = requests.get(URL)
    if response.status_code == 200:
        weather_data = response.json()
        print(json.dumps(weather_data, indent=4))
        return weather_data
    else:
        print("Error fetching weather data:", response.status_code)
        return None

class TestAPI(unittest.TestCase):
    @patch("requests.get")
    def test_get_station_info(self, mock_get):
        '''Testing the get_station_info function: testing static station infos'''
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"number": 225, "name": "EMMET ROAD"}]
        mock_get.return_value = mock_response

        result = get_station_info()

        mock_get.assert_called_once_with(
            STATIONS_URI,
            params={"apiKey": JCKEY, "contract": Contract_NAME}
        )
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["number"], 225)
        self.assertNotEqual(result[0]["number"],224)
        self.assertEqual(result[0]["name"], 'EMMET ROAD')
        self.assertNotEqual(result[0]["name"], 'WILTON TERRACE')

    @patch("requests.get")
    def test_get_station_info_failure(self, mock_get):
        '''Test failed API response for get_station_info'''
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = get_station_info()
        self.assertIsNone(result)

    @patch("requests.get")
    def test_get_weather_success(self, mock_get):
        '''Test successful API response for get_weather'''
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"weather": [
        {"id": 701,"main": "Mist","description": "mist","icon": "50n"}]}
        mock_get.return_value = mock_response

        result = get_weather()

        mock_get.assert_called_once_with(URL)
        self.assertIsInstance(result, dict)
        self.assertNotEqual(result["weather"][0]["main"], "Clouds")
        self.assertEqual(result["weather"][0]["main"], "Mist")

    @patch("requests.get")
    def test_get_weather_failure(self, mock_get):
        '''Test failed API response for get_weather'''
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = get_weather()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()