from flask import render_template
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
            light_intensity INT,
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
    
    cursor.execute("SELECT temp, hum, light_intensity, on_off FROM temp_hum_data ORDER BY rowid DESC LIMIT 5")
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        data = []
        for row in rows:
            data.append({
                "temp": row[0],
                "hum": row[1],
                "light_intensity": row[2],
                "on_off": bool(row[3])
            })
        return {"data": data}  # Return a list of rows as 'data'
    
    return {"error": "No data available"}

def list_database():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM temp_hum_data")
    
    rows = cur.fetchall()
    return render_template("list_database.html", rows=rows)

def insert_sensor_data(temp, hum, light_intensity, on_off):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO temp_hum_data (temp, hum, light_intensity, on_off) VALUES (?, ?, ?, ?)", 
                       (temp, hum, light_intensity, on_off))
        conn.commit()
        return {"message:": "Sensor data inserted suvvessfully"}
    
    except sqlite3.Error as e:
        return {"error": f"Database error: {e}"}
    
    finally:
        conn.close()

def insert_test_data():
    try:
        import random
    except ImportError as e:
        print(f"Import error: {e}")

    conn = get_db_connection()
    cursor = conn.cursor()
    for i in range(5):
        temp = round(random.uniform(15, 30), 2)
        hum = round(random.uniform(30, 80), 2) 
        light_intensity = random.randint(0, 1023)
        on_off = random.choice([0, 1])

        cursor.execute("INSERT INTO temp_hum_data (temp, hum, light_intensity, on_off) VALUES (?, ?, ?, ?)", 
                    (temp, hum, light_intensity, on_off))

        conn.commit()
    conn.close()
    return {"message": "Test data inserted", "temp": temp, "hum": hum, "light_intensity": light_intensity, "on_off": on_off}
        