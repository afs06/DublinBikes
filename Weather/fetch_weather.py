# 调用OpenWeather API
# 使用 requestes 获取天气数据
# 获取天气数据失败提示
# 抓取 json数据

import requests
import json

API_KEY = "7226a2c4ce82265fde9c8d32f42258ec"
CITY = "Dublin"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def get_weather():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching weather data:", response.status_code)
        return None

if __name__ == "__main__":
    weather_data = get_weather()
    if weather_data:
        print(json.dumps(weather_data, indent=4))
