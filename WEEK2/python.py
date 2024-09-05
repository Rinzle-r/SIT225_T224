import serial
import csv
from datetime import datetime

ser = serial.Serial('COM9', 9600)

with open('DHT11_data.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(['timestamp', 'temperature', 'humidity'])

    while True:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith('DHT11'):
            data = line.split(',')
            temperature = data[1]
            humidity = data[2]
            
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            
            writer.writerow([timestamp, temperature, humidity])
            
            print(f"Timestamp >> {timestamp}, Temperature >> {temperature}, Humidity >> {humidity}")
