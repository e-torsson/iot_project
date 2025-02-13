from flask import Flask, render_template, jsonify, g
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
    return "input data"

@app.route('/list')
def list_db():
    return database.list_database()

@app.route('/get_latest_data')
def view_data():
    data = database.get_latest_data()
    return jsonify(data)

@app.route('/insert_test_data')
def insert_test():
    """Flask route to insert test sensor data."""
    data = database.insert_test_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run()