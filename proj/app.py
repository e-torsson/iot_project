from flask import Flask, render_template, jsonify, request, redirect
import database

app = Flask(__name__)



@app.route('/')
def first_page():
    return render_template("first_page.html")

@app.route('/createdb')
def createdb():
    try:
        database.create_db()
        return "Database Created Successfully"
    except Exception as e:
        print(f"Something went wrong creating database: {e}")


@app.route('/input_data')
def input_data():
    data = database.insert_test_data()
    return jsonify(data)


@app.route('/list')
def list_db():
    return database.list_database()

@app.route('/get_latest_data')
def view_data():
    data = database.get_latest_data()
    return jsonify(data)

@app.route('/send_sensor_data', methods=['POST'])
def send_sensor_data():
    try:
        data = request.get_json()
        
        temp = data.get("temp")
        hum = data.get("hum")
        light_intensity = data.get("light_intensity")
        on_off = data.get("on_off")
        
        if None in (temp, hum, light_intensity, on_off):
            return jsonify({"error": "Missing data"}), 400
        
        response = database.insert_sensor_data(temp, hum, light_intensity, on_off)
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500

# @app.route('/input_data')
# def insert_test():
#     """Flask route to insert test sensor data."""
#     data = database.insert_test_data()
#     return jsonify(data)

if __name__ == "__main__":
    app.run()