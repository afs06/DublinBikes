# current weather download - json

import requests
import json
import pymysql
import time
import datetime
import os
from pymysql import Error

# 改用 current weather API 而不是 forecast API
API_KEY = "7226a2c4ce82265fde9c8d32f42258ec"
CITY = "Dublin"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def connect_db():
    try:
        connection = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="Chennan520!",
            database="current_weather",
            charset="utf8mb4"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def extract_current_weather(json_text):
    try:
        data = json.loads(json_text)
        return {
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None

def write_to_db(data):
    if not data:
        print("No data to write to database")
        return False

    conn = None
    cursor = None
    try:
        conn = connect_db()
        if not conn:
            return False

        cursor = conn.cursor()

        sql = """INSERT INTO weather 
                 (timestamp, city, temperature, feels_like, humidity, wind_speed)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        
        values = (
            data["timestamp"],
            CITY,
            data["temperature"],
            data["feels_like"],
            data["humidity"],
            data["wind_speed"]
        )
        
        cursor.execute(sql, values)
        conn.commit()
        print(f"Successfully inserted weather data for {data['timestamp']}")
        return True

    except Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def main():
    if not os.path.exists("data"):
        os.mkdir("data")

    while True:
        try:
            current_time = datetime.datetime.now()
            print(f"\nFetching current weather data at {current_time}")
            
            response = requests.get(URL)
            if response.status_code == 200:
                json_data = response.text

                # 保存 JSON 到文件
                filename = f"data/weather_{current_time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
                with open(filename, "w") as f:
                    f.write(json_data)
                print(f"Weather data saved to {filename}")

                # 解析并存入数据库
                weather_data = extract_current_weather(json_data)
                if weather_data:
                    success = write_to_db(weather_data)
                    if success:
                        print("Data successfully written to database")
                    else:
                        print("Failed to write data to database")
                else:
                    print("No data extracted from API response")
            else:
                print(f"Error fetching weather data: {response.status_code}")

            # 休眠3600分钟 - 1小时
            print(f"Sleeping for a hour until next update...")
            time.sleep(3600)  # 一小时 = 3600秒

        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(60)  # 发生错误时等待1分钟后重试

if __name__ == "__main__":
    main()