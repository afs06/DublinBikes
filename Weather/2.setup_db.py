# 创建 MySQL 数据库和表

import pymysql
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# 数据库连接信息
USER = "root"
PASSWORD = "Chennan520!"
PORT = "3306"
DB = "current_weather"
URI = "127.0.0.1"

# 创建数据库连接
encoded_password = quote_plus(PASSWORD)
connection_string = f"mysql+pymysql://{USER}:{PASSWORD}@{URI}:{PORT}"
engine = create_engine(connection_string, echo=True)

# 创建数据库（如果不存在）
with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB}"))
    conn.commit()  # 确保变更生效

# 连接到新创建的数据库
connection_string = f"mysql+pymysql://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}"
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

# 执行 SQL 语句
with engine.connect() as conn:
    conn.execute(text(sql))
    conn.commit()  # 在 with 语句块中调用 commit

print("Database and table setup complete!")
