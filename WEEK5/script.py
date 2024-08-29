import serial
import time
import firebase_admin
from firebase_admin import credentials, db


cred = credentials.Certificate("task.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://week5-ardi-default-rtdb.firebaseio.com/'
})

arduino = serial.Serial('COM9', 9600) 
data_duration = 30 * 60  
starting_time = time.time()

while True:
    if time.time() - starting_time > data_duration:
        break

    if arduino.in_waiting > 0:
        data = arduino.readline().decode('utf-8').strip()
        timestamp = int(time.time() * 1000)  
        x, y, z = map(float, data.split(','))  

        json_data = {
            'timestamp': timestamp,
            'x': x,
            'y': y,
            'z': z
        }

        ref = db.reference('gyroscope_data')
        ref.push(json_data)

        print(f"Data sent >> {json_data}")

    time.sleep(10)

arduino.close()
