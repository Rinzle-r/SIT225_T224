#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>
#include <DHT.h>  

#define DHTPIN 2       // Pin for DHT11
#define DHTTYPE DHT11  // DHT11 sensor

const char SSID[]  = "VodafonePocketWiFi4-DDC3";  
const char PASS[]  = "hD9D37eLNL6";

DHT dht(DHTPIN, DHTTYPE);  

float temp;  // Temperature variable
float humi;  // Humidity variable
bool alarmLED = false;  // LED for alarm 
void initProperties() 
{
  ArduinoCloud.addProperty(temp, READ, ON_CHANGE, NULL);  
  ArduinoCloud.addProperty(humi, READ, ON_CHANGE, NULL); 
  ArduinoCloud.addProperty(alarmLED, READWRITE, ON_CHANGE, NULL);  
}

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);

void setup() 
{
  Serial.begin(9600);  
  dht.begin();  
  initProperties();  

  ArduinoCloud.begin(ArduinoIoTPreferredConnection);  
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();  
}

void loop() 
{
  ArduinoCloud.update(); 
  
  temp = dht.readTemperature();  
  humi = dht.readHumidity();  
  
  if (isnan(temp) || isnan(humi)) 
  {
    Serial.println("Error!!! Issue in reading data from DHT sensor");
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.print(" °C, Humidity: ");
  Serial.print(humi);
  Serial.println(" %");

  if (temp > 35 || humi > 50)
  {
    alarmLED = true;  
  }

  delay(5000);  
}
