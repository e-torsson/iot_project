import sqlite3

try:
    conn = sqlite3.connect('sensor_data.db')
    print("Database opened successfully")
except:
    print("Error: unable to connect to database")
    
def data(temp, hum, time, on_off):
    conn.execute(f"INSERT INTO temp_hum_data VALUES ({temp}, {hum}, {time}, {on_off})")
    conn.commit()
    