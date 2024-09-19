#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>
#include <DHT.h>  

#define DHTPIN 2        
#define DHTTYPE DHT11   

const char SSID[]  = "VodafonePocketWiFi4-DDC3";    
const char PASS[]  = "hD9D37eLNL6";
DHT dht(DHTPIN, DHTTYPE);  

float temp;    // Changed from temperature to temp
float humi;    // Changed from humidity to humi

void initProperties()
{
  ArduinoCloud.addProperty(temp, READ, ON_CHANGE, NULL);  // Changed to temp
  ArduinoCloud.addProperty(humi, READ, ON_CHANGE, NULL);  // Changed to humi
}

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);

void setup() 
{
  Serial.begin(9600);
  delay(1500); 
  dht.begin();  
  initProperties();  
  
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() 
{
  ArduinoCloud.update();
  temp = dht.readTemperature();   // Changed to temp
  humi = dht.readHumidity();      // Changed to humi

  if (isnan(temp) || isnan(humi))  // Changed to temp and humi
  {
    Serial.println("Error!!!, issue reading data from DHT sensor");
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temp);             // Changed to temp
  Serial.print(" °C, Humidity: ");
  Serial.print(humi);             // Changed to humi
  Serial.println(" %");

  delay(5000);  
}
