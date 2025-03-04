# 访问 API：
# http://127.0.0.1:5000/api/weather
# http://127.0.0.1:5000/api/update_weather (POST 请求) - terminal: curl -X POST http://127.0.0.1:5000/api/update_weather


from flask import Flask, jsonify, g, request, session, redirect, url_for
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import pymysql
import os
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_secret')  # 设定 SECRET_KEY

# 1. 模拟用户数据库
# 登录并存储 session - terminal
# curl -X POST -d "username=joy&password=814742090" -c cookies.txt http://127.0.0.1:5000/login
# 使用相同的 session 访问 /api/weather - terminal
# curl -X GET -b cookies.txt http://127.0.0.1:5000/api/weather

users = {
    'joy': {'password': '814742090', 'name': 'Joy'},
    'chen': {'password': 'chen', 'name': 'Chen'},
}

# 2. 登录接口
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in users and users[username]['password'] == password:
        session['username'] = username  # 登录成功，存入 session
        return jsonify({'message': 'Login successful!'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# 3. 退出登录
@app.route('/logout')
def logout():
    session.pop('username', None)
    return jsonify({'message': 'You have been logged out.'})

# 4. 保护 API：检查用户是否登录
from functools import wraps  # ✅ 加入这个

def login_required(f):
    @wraps(f)  # ✅ 这里加上 wraps，保持原始函数信息
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'You must be logged in'}), 403
        return f(*args, **kwargs)
    return wrapper

# 5. 个人资料页面
@app.route('/profile')
@login_required
def profile():
    username = session['username']
    return jsonify({'message': f'Welcome to your profile, {users[username]["name"]}!'})

# 6. 连接 MySQL
USER = "root"
PASSWORD = "Chennan520!"
PORT = "3306"
DB = "current_weather"
URI = "127.0.0.1"

def connect_to_db():
    encoded_password = quote_plus(PASSWORD)
    connection_string = f"mysql+pymysql://{USER}:{encoded_password}@{URI}:{PORT}/{DB}"
    engine = create_engine(connection_string, echo=True)
    return engine

def get_db():
    db_engine = getattr(g, '_database', None)
    if db_engine is None:
        db_engine = g._database = connect_to_db()
    return db_engine

# 7. 仅限登录用户访问天气数据
@app.route('/api/weather', methods=['GET'])
@login_required
def get_weather():
    engine = get_db()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM weather ORDER BY timestamp DESC LIMIT 1;"))  
    weather_data = [dict(row._mapping) for row in rows]
    return jsonify(weather_data)

# 8. 更新天气数据（管理员权限）
@app.route('/api/update_weather', methods=['POST'])
@login_required
def update_weather():
    if session.get('username') != 'joy':  # 仅 joy（管理员）能更新
        return jsonify({'error': 'Admin access required'}), 403

    API_KEY = "7226a2c4ce82265fde9c8d32f42258ec"
    CITY = "Dublin"
    API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

    response = requests.get(API_URL)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather data"}), 500

    weather_data = response.json()
    city = weather_data["name"]
    temperature = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]

    conn = pymysql.connect(host=URI, user=USER, password=PASSWORD, database=DB)
    cursor = conn.cursor()
    sql = """
    INSERT INTO weather (city, temperature, feels_like, humidity, wind_speed) 
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (city, temperature, feels_like, humidity, wind_speed))
    conn.commit()
    conn.close()

    return jsonify({"message": "Weather data updated successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
