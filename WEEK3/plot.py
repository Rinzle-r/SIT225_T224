import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load cleaned data
df = pd.read_csv('cleaned_sensor_data.csv')

# Convert 'Timestamp' column to datetime format (ISO 8601)
df['Timestamp'] = pd.to_datetime(df['Timestamp'], utc=True)

# Combined plot
plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['Temperature'], label='Temperature', color='red')
plt.plot(df['Timestamp'], df['Humidity'], label='Humidity', color='orange')

# Formatting the plot
plt.xlabel('Timestamp')
plt.ylabel('Values')
plt.title('Temperature and Humidity over Time')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Use DateFormatter for x-axis labels to control their format
ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

# Reduce the number of ticks on the x-axis
ax.xaxis.set_major_locator(mdates.AutoDateLocator())

# Enable grid
plt.grid(True)

# Ensure layout is not cramped
plt.tight_layout()

# Add legend
plt.legend()

# Show plot
plt.show()
