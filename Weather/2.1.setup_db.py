# 创建 MySQL 数据库和表

import pymysql
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# 数据库连接信息
USER = "zhuowen"
PASSWORD = "814742090"
PORT = "3306"
DB = "current_weather"
URI = "db-weather.cd4ky0msa8j7.eu-north-1.rds.amazonaws.com"

# 对密码进行编码
encoded_password = quote_plus(PASSWORD)

# 创建数据库连接
connection_string = f"mysql+pymysql://{USER}:{encoded_password}@{URI}:{PORT}"
# 创建数据库连接引擎
engine = create_engine(connection_string, echo=True)

# 创建数据库（如果不存在）
with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB}"))
    conn.commit()  # 确保变更生效

# 连接到新创建的数据库
connection_string = f"mysql+pymysql://{USER}:{encoded_password}@{URI}:{PORT}/{DB}"
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
    conn.commit()

print("Database and table setup complete!")
