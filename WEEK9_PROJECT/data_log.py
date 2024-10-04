import firebase_admin
from firebase_admin import credentials, db
import serial
import time

# Initialize Firebase Admin SDK
cred = credentials.Certificate("pro.json")  
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://arduinoproject-a7c52-default-rtdb.firebaseio.com/'  # Firebase DB URL
})

# Open the serial connection to Arduino
arduino = serial.Serial('COM9', 9600)  

# Main loop to read data and send it to Firebase
while True:
    # Check if there is incoming data from Arduino
    if arduino.in_waiting > 0:
        # Reading data from Arduino. Data format is expected to be CSV: temperature, humidity, soil_moisture
        data = arduino.readline().decode('utf-8').strip()

        # Debug: Print the raw data received from Arduino
        print(f"Raw data from Arduino: {data}")
        
        # Split the data into temperature, humidity, and soil moisture
        try:
            # Ensure the data has exactly three comma-separated values
            temp, humidity, soil_moisture = map(float, data.split(','))
        except ValueError:
            # Error parsing data, log it and skip
            print(f"Error parsing data from Arduino: {data}. Skipping this entry.")
            continue
        
        # Prepare the data to be sent to Firebase
        sensor_data = {
            'timestamp': int(time.time() * 1000),  # current timestamp in milliseconds
            'temperature': temp,
            'humidity': humidity,
            'soil_moisture': soil_moisture
        }

        # Send the data to Firebase under the "sensor_data" node
        ref = db.reference('sensor_data')
        ref.push(sensor_data)

        print(f"Data sent to Firebase: {sensor_data}")
    
    # Delay between readings (5 seconds in this example)
    time.sleep(5)
