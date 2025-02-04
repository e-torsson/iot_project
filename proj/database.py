import sqlite3
import os

DATABASE_PATH = os.path.abspath("../sensor_data.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    conn = get_db_connection()
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS temp_hum_data (
            temp FLOAT,
            hum FLOAT,
            time TEXT,
            on_off INT)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()
        
def get_latest_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='temp_hum_data'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        conn.close()
        return {"error": "Database not initialized"}
    
    cursor.execute("SELECT temp, hum, time, on_off FROM temp_hum_data ORDER BY time DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return{
            "temp": row[0],
            "hum": row[1],
            "time": row[2],
            "on_off": bool(row[3])
        }
    return {"error": "No data available"}