import pymysql
from fetch_weather import get_weather

USER = "root"
PASSWORD = "Chennan520!"
PORT = "3306"
DB = "current_weather"
URI = "127.0.0.1"

def store_weather():
    weather_data = get_weather()
    if not weather_data:
        return

    city = weather_data["name"]
    temperature = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]

    conn = pymysql.connect(host=URI, user=USER, password=PASSWORD, database=DB)
    cursor = conn.cursor()
    sql = "INSERT INTO weather (city, temperature, feels_like, humidity, wind_speed) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (city, temperature, feels_like, humidity, wind_speed))

    conn.commit()
    conn.close()
    print("Weather data stored successfully!")

if __name__ == "__main__":
    store_weather()
