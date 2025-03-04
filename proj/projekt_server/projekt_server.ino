#include "WiFiS3.h"
#include "arduino_secrets.h"
#include <ArduinoJson.h>
#include <DHT.h>
#include <Wire.h>



// WiFi Cred
const char* ssid = SECRET_SSID;
const char* password = SECRET_PASS;
const char* server = "192.168.0.229";  // Flask server
int port = 5000;

WiFiClient client;

// DHT Sensor Setup
#define DHTPIN 5
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// LED Setup
#define LEDPIN 12

// LDR Setup
#define LIGHT_SENSOR_PIN A5

void sendSensorData(float temp, float hum, int lightIntensity, int on_off) {
  if (client.connect(server, port)) {
    Serial.println("Connected to server!");

    // JSON object
    StaticJsonDocument<200> jsonDoc;
    jsonDoc["temp"] = temp;
    jsonDoc["hum"] = hum;
    jsonDoc["light_intensity"] = lightIntensity;
    jsonDoc["on_off"] = on_off;

    // JSON to string
    String jsonString;
    serializeJson(jsonDoc, jsonString);

    // Send HTTP POST request
    client.println("POST /send_sensor_data HTTP/1.1");
    client.println("Host: " + String(server));
    client.println("Content-Type: application/json");
    client.println("Content-Length: " + String(jsonString.length()));
    client.println();
    client.println(jsonString);

    Serial.println("Data sent: " + jsonString);
  } else {
    Serial.println("Connection failed!");
  }

  client.stop();
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected!");

  // Initialize DHT sensor
  dht.begin();

  // LED pin as output
  pinMode(LEDPIN, OUTPUT);

  pinMode(LIGHT_SENSOR_PIN, INPUT);
}

void loop() {
  // Read temperature and humidity
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  // Check if readings are valid
  if (isnan(temp) || isnan(hum)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  int lightIntensity = analogRead(LIGHT_SENSOR_PIN);

  // Control LED based on temperature
  int on_off = (temp >= 26) ? 1 : 0;
  digitalWrite(LEDPIN, on_off);

  // Send data to Flask server
  sendSensorData(temp, hum, lightIntensity, on_off);

  Serial.print("Temp: ");
  Serial.print(temp);
  Serial.print("°C, Humidity: ");
  Serial.print(hum);
  Serial.print("%, Light Intensity: ");
  Serial.println(lightIntensity);

  delay(5000);
}
