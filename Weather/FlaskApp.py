from flask import Flask, jsonify, g
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

app = Flask(__name__)

# 数据库连接信息
USER = "root"
PASSWORD = "Chennan520!"
PORT = "3306"
DB = "current_weather"
URI = "127.0.0.1"

# 创建数据库连接
def connect_to_db():
    encoded_password = quote_plus(PASSWORD)
    connection_string = f"mysql+pymysql://{USER}:{encoded_password}@{URI}:{PORT}/{DB}"
    engine = create_engine(connection_string, echo=True)
    return engine

# Show all stations in json
@app.route('/OpenWeather')
def get_weather():
    engine = get_db()

    OpenWeather = []
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * from weather;"))  # weather is the name of the table in the db

    for row in rows:
        OpenWeather.append(dict(row._mapping))

    return jsonify(OpenWeather=OpenWeather)

def get_db():
    db_engine = getattr(g, '_database', None)
    if db_engine is None:
        db_engine = g._database = connect_to_db()
    return db_engine

@app.route('/dublinbike')
def hello():
    return 'Navigate http://127.0.0.1:5000/OpenWeather'

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

# 创建数据库和表（如果不存在）
def setup_database():
    engine = connect_to_db()
    
    # 创建数据库（如果不存在）
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB}"))
        conn.commit()

    # 连接到新创建的数据库
    connection_string = f"mysql+pymysql://{USER}:{quote_plus(PASSWORD)}@{URI}:{PORT}/{DB}"
    engine = create_engine(connection_string, echo=True)

    # 创建 weather 表
    sql = """
    CREATE TABLE IF NOT EXISTS weather (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city VARCHAR(50),
        temperature FLOAT,
        feels_like FLOAT,
        humidity INT,
        wind_speed FLOAT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

    print("Database and table setup complete!")

# 仅在首次运行时调用该函数来设置数据库
setup_database()
