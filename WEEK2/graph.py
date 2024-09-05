import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('DHT11_data.csv')
df = df.dropna()  
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
df = df.dropna()  

df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
plt.figure(figsize=(12, 6))

# Plotting temperature
plt.subplot(2, 1, 1)
plt.plot(df['timestamp'], df['temperature'], label='Temperature', color='blue')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.title(' >> Temperature over Time << ')
plt.legend()

# Plotting humidity
plt.subplot(2, 1, 2)
plt.plot(df['timestamp'], df['humidity'], label='Humidity', color='orange')
plt.xlabel('Time')
plt.ylabel('Humidity')
plt.title(' >> Humidity over Time <<')
plt.legend()

plt.tight_layout()
plt.savefig('sensor_plot.png')
plt.show()
