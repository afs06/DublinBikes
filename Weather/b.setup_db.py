from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

USER = "root"
PASSWORD = "Chennan520!"
PORT = "3306"
DB = "current_weather"
URI = "127.0.0.1"

def connect_to_db():
    encoded_password = quote_plus(PASSWORD)
    connection_string = f"mysql+pymysql://{USER}:{encoded_password}@{URI}:{PORT}/{DB}"
    return create_engine(connection_string, echo=True)

def setup_database():
    engine = connect_to_db()
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB}"))
        conn.commit()

    engine = connect_to_db()
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

if __name__ == "__main__":
    setup_database()
