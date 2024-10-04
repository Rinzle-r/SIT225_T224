#include <DHT.h>
#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>

// Define sensor pins and types
#define DHTPIN 2         
#define DHTTYPE DHT11    
#define SOIL_MOISTURE_PIN A0  // Analog pin connected to Soil Moisture Sensor

// Initialize DHT sensor
DHT dht(DHTPIN, DHTTYPE);

// WiFi Credentials
const char SSID[] = "VodafonePocketWiFi4-DDC3"; 
const char PASS[] = "hD9D37eLNL6"; 

// Variables to store sensor data
float temperature = 0;
float humidity = 0;
int soilMoisture = 0;

// Arduino Cloud Properties
void initProperties() {
  ArduinoCloud.addProperty(temperature, READ, ON_CHANGE, NULL);
  ArduinoCloud.addProperty(humidity, READ, ON_CHANGE, NULL);
  ArduinoCloud.addProperty(soilMoisture, READ, ON_CHANGE, NULL);
}

// WiFi Connection Handler
WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);

void setup() {
  Serial.begin(9600);
  
  delay(2000);  // 2 second delay for sensor to stabilize
  dht.begin();
  
  // Initialize Arduino Cloud
  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
}

void loop() {
  // Updating Arduino Cloud
  ArduinoCloud.update();
  
  // Reading sensor data
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  soilMoisture = analogRead(SOIL_MOISTURE_PIN);
  
  // Check if any reads failed
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!!!");
    return;
  }
  
  // Send data (temperature,humidity,soil_moisture)
  Serial.print(temperature);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.println(soilMoisture);
  
  delay(10000);  // Delay of 10 seconds before next reading
}
