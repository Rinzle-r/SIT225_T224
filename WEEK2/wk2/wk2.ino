#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11  
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("ERROR!!!");
    return;
  }

  Serial.print("DHT11,");
  Serial.print(temperature);
  Serial.print(",");
  Serial.println(humidity);

  delay(30000); 
