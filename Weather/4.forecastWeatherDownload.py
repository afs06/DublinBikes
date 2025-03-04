import requests
import json
import pymysql
import time
import datetime
import os
from pymysql import Error

# API 相关信息
API_KEY = "7226a2c4ce82265fde9c8d32f42258ec"
CITY = "Dublin"
URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

# 创建数据文件夹
if not os.path.exists("data"):
    os.mkdir("data")

# 连接 MySQL 数据库
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

# 解析 JSON 并提取天气数据
def extract_info(json_text):
    try:
        data = json.loads(json_text)
        extracted_data = []
        
        for entry in data["list"]:
            extracted_data.append({
                "timestamp": entry["dt_txt"],
                "temperature": entry["main"]["temp"],
                "feels_like": entry["main"]["feels_like"],
                "humidity": entry["main"]["humidity"],
                "wind_speed": entry["wind"]["speed"]
            })
        
        return extracted_data
    except Exception as e:
        print(f"Error extracting data: {e}")
        return []

# 插入数据到 MySQL
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
        
        success_count = 0
        for entry in data:
            try:
                values = (
                    entry["timestamp"],
                    CITY,
                    entry["temperature"],
                    entry["feels_like"],
                    entry["humidity"],
                    entry["wind_speed"]
                )
                cursor.execute(sql, values)
                success_count += 1
            except Error as e:
                print(f"Error inserting record: {e}")
                continue

        conn.commit()
        print(f"Successfully inserted {success_count} out of {len(data)} records")
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

# 定期获取数据
def main():
    while True:
        try:
            print(f"\nFetching weather data at {datetime.datetime.now()}")
            
            response = requests.get(URL)
            if response.status_code == 200:
                json_data = response.text

                # 保存 JSON 到文件
                now = datetime.datetime.now()
                filename = f"data/weather_{now.strftime('%Y-%m-%d_%H-%M-%S')}.json"
                with open(filename, "w") as f:
                    f.write(json_data)
                print(f"Weather data saved to {filename}")

                # 解析并存入数据库
                extracted_data = extract_info(json_data)
                if extracted_data:
                    success = write_to_db(extracted_data)
                    if success:
                        print("Data successfully written to database")
                    else:
                        print("Failed to write data to database")
                else:
                    print("No data extracted from API response")

            else:
                print(f"Error fetching weather data: {response.status_code}")

            # 休眠10分钟
            print(f"Sleeping for 10 minutes until next update...")
            time.sleep(600)  # 10分钟 = 600秒

        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(60)  # 发生错误时等待1分钟后重试

if __name__ == "__main__":
    main()

    