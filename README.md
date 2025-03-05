# Sensor Dashboard

## Description
This is a Flask-based web application that displays real-time sensor data for temperature, humidity, and light intensity. The project allows users to insert test data, and view stored sensor readings.

## Features
- Live updates of sensor data (Temperature, Humidity, Light Intensity).
- SQLite database to store sensor readings.
- Responsive web interface with HTML, CSS, and JavaScript.

## Software
### Prerequisites
- Python 3.x
- Flask
- SQLite
- Arduino IDE (To upload code to Arduino)

## Hardware
### Prerequisites
- Arduino UNO R4 WiFi
- DHT11 Temperature and Humidity Sensor
- LDR (Light Dependent Resistor) Sensor
- LED
- Breadboard (Optional) and Jumper Wires


### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/e-torsson/iot_project.git
   cd proj
2. Install the required packages:
    ```bash
    pip install flask sqlite3
3. Start the Flask application:
    ```bash
    flask --run --host=0.0.0.0 --port 5000

## Usage
Open a web browser and navigate to `http://localhost:5000/` to access

### Different pages
- **Home (/)**: Displays the latest 5 sensor readings (including dummy data).
- **View Database (/list_database)**: See all stored sensor readings.
- **Create Database (/create_database)**: Initialize the database
- **Insert Data (/insert_data)**: Insert new randomized sensor readings into the database (mostly for debugging purposes).

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask, SQLite
- **Hardware**: Arduino UNO R4 WiFi, DHT11, LDR, LED,
- **IDE**: Arduino IDE, Visual Studio Code (for Python development)