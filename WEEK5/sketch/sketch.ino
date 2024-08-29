#include <Arduino_LSM6DS3.h>

void setup() 
{
  Serial.begin(9600);
  
  if (!IMU.begin()) 
  {
    Serial.println("Error");
    while (1);
  }
}

void loop() 
{
  if (IMU.gyroscopeAvailable())
  {
    float x, y, z;
    
    IMU.readGyroscope(x, y, z);
    
    Serial.print(x);
    Serial.print(",");
    Serial.print(y);
    Serial.print(",");
    Serial.println(z);
  }
  
  delay(1000); 
}
